# Webbdelen för Lennarts matstation. Coolify bygger den här filen vid varje deploy.
FROM python:3.12-slim

# Kör inte som root i containern.
RUN useradd --create-home --uid 10001 lennart
WORKDIR /app
COPY app.py index.html ./
USER lennart

ENV PORT=8000 PYTHONUNBUFFERED=1
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3).status == 200 else 1)"

CMD ["python", "app.py"]
