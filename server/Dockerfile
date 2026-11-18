# Webbdelen för Lennarts matstation. Coolify bygger den här filen vid varje deploy.
FROM python:3.12-slim

# curl behövs för Coolifys hälsokontroll, som anropar /healthz med curl eller wget.
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Kör inte som root i containern.
RUN useradd --create-home --uid 10001 lennart \
 && mkdir /data && chown lennart /data
WORKDIR /app
COPY app.py admin.py live.py clips.py index.html demo.html admin.html login.html clips.html ./
COPY static ./static
USER lennart

# Inställningarna sparas i /data. Montera en volym där i Coolify, så att de överlever en deploy.
ENV PORT=8000 PYTHONUNBUFFERED=1 DATA_DIR=/data
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3).status == 200 else 1)"

# Coolify kan skicka med vilken commit som byggs ("Include Source Commit in Build").
# Läggs sist, så att resten av bygget kan återanvändas från cache.
ARG SOURCE_COMMIT=""
ENV SOURCE_COMMIT=${SOURCE_COMMIT}

CMD ["python", "app.py"]
