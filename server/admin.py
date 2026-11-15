"""Inloggning till adminvyn på lennart.cam.

- Lösenordet ligger i miljövariabeln ADMIN_PASSWORD i Coolify, aldrig i repot.
- Efter inloggning får webbläsaren en slumpmässig sessionskaka som bara servern
  känner till. Kakan är HttpOnly (JavaScript kommer inte åt den), Secure (bara
  över https) och SameSite=Strict (skickas inte med från andra webbplatser).
- Efter för många felaktiga försök spärras inloggningen en stund.
"""

import hashlib
import hmac
import os
import secrets
import threading
import time

def _clean(value: str) -> str:
    """Ta bort mellanslag, radbrytningar och omslutande citattecken som lätt följer med vid inklistring."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    return value


ADMIN_PASSWORD = _clean(os.environ.get("ADMIN_PASSWORD", ""))
COOKIE_NAME = "lennart_admin"
SESSION_S = 12 * 3600
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "1") != "0"  # 0 bara vid test utan https

FAIL_WINDOW_S = 15 * 60
MAX_FAILS_PER_IP = 5
MAX_FAILS_TOTAL = 30  # skydd även om någon försöker från många adresser

_lock = threading.Lock()
_sessions: dict[str, float] = {}       # kaka -> giltig till (i minnet, nollställs vid deploy)
_fails: dict[str, list[float]] = {}    # ip -> tidpunkter för felaktiga försök


def fingerprint(value: str) -> str:
    """De första 6 tecknen av SHA-256. Avslöjar inget användbart om ett långt slumpmässigt
    lösenord, men gör det möjligt att se om två lösenord är samma."""
    return hashlib.sha256(value.encode()).hexdigest()[:6]


def enabled() -> bool:
    return bool(ADMIN_PASSWORD)


def _recent(times: list[float], now: float) -> list[float]:
    return [t for t in times if now - t < FAIL_WINDOW_S]


def locked_out(ip: str) -> bool:
    now = time.time()
    with _lock:
        for key in list(_fails):
            _fails[key] = _recent(_fails[key], now)
            if not _fails[key]:
                del _fails[key]
        total = sum(len(v) for v in _fails.values())
        return len(_fails.get(ip, [])) >= MAX_FAILS_PER_IP or total >= MAX_FAILS_TOTAL


def check_password(ip: str, password: str) -> bool:
    ok = enabled() and hmac.compare_digest(password.strip().encode(), ADMIN_PASSWORD.encode())
    if not ok:
        with _lock:
            _fails.setdefault(ip, []).append(time.time())
        time.sleep(1)  # gör det långsamt att gissa
    return ok


def new_session() -> str:
    token = secrets.token_urlsafe(32)
    with _lock:
        _sessions[token] = time.time() + SESSION_S
    return token


def end_session(token: str | None) -> None:
    if token:
        with _lock:
            _sessions.pop(token, None)


def valid(token: str | None) -> bool:
    if not token:
        return False
    with _lock:
        expires = _sessions.get(token)
        if expires is None:
            return False
        if expires < time.time():
            del _sessions[token]
            return False
        return True


def cookie_header(token: str, max_age: int = SESSION_S) -> str:
    parts = [f"{COOKIE_NAME}={token}", "Path=/", f"Max-Age={max_age}", "HttpOnly", "SameSite=Strict"]
    if COOKIE_SECURE:
        parts.append("Secure")
    return "; ".join(parts)


def token_from_cookie(cookie_header_value: str | None) -> str | None:
    for part in (cookie_header_value or "").split(";"):
        name, _, value = part.strip().partition("=")
        if name == COOKIE_NAME and value:
            return value
    return None
