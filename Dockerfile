FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    AURA_DATA_DIR=/var/aura

WORKDIR /app

# системные зависимости для weasyprint (PDF) + шрифты
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 \
      libcairo2 libgdk-pixbuf2.0-0 shared-mime-info \
      fonts-dejavu && \
    rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app
# каталог для логов/экспортов
RUN mkdir -p /var/aura && adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /var/aura /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

