# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt pyproject.toml config.yaml ./
COPY src/ src/

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir .

# Stage 2: Runtime
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 anny \
    && useradd --uid 1000 --gid anny --create-home anny \
    && mkdir -p /home/anny/.anny && chown anny:anny /home/anny/.anny

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=builder /app/src src
COPY --from=builder /app/config.yaml .

USER anny

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.anny.main:app", "--host", "0.0.0.0", "--port", "8000"]
