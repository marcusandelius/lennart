"""Inloggning till adminvyn på lennart.cam.

- Lösenordet ligger i miljövariabeln ADMIN_PASSWORD i Coolify, aldrig i repot.
- Efter inloggning får webbläsaren en sessionskaka som gäller i 30 dagar. Kakan är
  signerad (HMAC-SHA256) med en nyckel som räknas fram ur ADMIN_PASSWORD, så servern
  behöver inte spara sessionerna. Därför överlever inloggningen en omstart eller
  deploy. Byts lösenordet blir alla gamla kakor ogiltiga.
- Kakan är HttpOnly (JavaScript kommer inte åt den), Secure (bara över https) och
  SameSite=Strict (skickas inte med från andra webbplatser).
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
SESSION_S = 30 * 24 * 3600  # 30 dagar
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "1") != "0"  # 0 bara vid test utan https

FAIL_WINDOW_S = 15 * 60
MAX_FAILS_PER_IP = 5
MAX_FAILS_TOTAL = 30  # skydd även om någon försöker från många adresser

_lock = threading.Lock()
_logged_out: set[str] = set()          # utloggade kakor fram till nästa omstart, se end_session()
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


def _key() -> bytes:
    """Nyckeln som signerar kakorna. Räknas fram ur lösenordet, så den är densamma efter
    en omstart men ändras om lösenordet byts."""
    return hmac.new(ADMIN_PASSWORD.encode(), b"lennart-admin-session-v1", hashlib.sha256).digest()


def _sign(payload: str) -> str:
    return hmac.new(_key(), payload.encode(), hashlib.sha256).hexdigest()


def new_session() -> str:
    """Kakans innehåll: giltig-till (unixtid), ett slumpvärde och signaturen."""
    payload = f"{int(time.time()) + SESSION_S}.{secrets.token_urlsafe(16)}"
    return f"{payload}.{_sign(payload)}"


def end_session(token: str | None) -> None:
    # Kakan tas bort i webbläsaren vid utloggning. Servern minns också att den är utloggad,
    # men bara fram till nästa omstart, eftersom inget sparas på disk.
    if token:
        with _lock:
            _logged_out.add(token)


def valid(token: str | None) -> bool:
    if not token or not enabled():
        return False
    payload, _, signature = token.rpartition(".")
    expires, _, _nonce = payload.partition(".")
    if not payload or not hmac.compare_digest(signature, _sign(payload)):
        return False
    try:
        if int(expires) < time.time():
            return False
    except ValueError:
        return False
    with _lock:
        return token not in _logged_out


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
