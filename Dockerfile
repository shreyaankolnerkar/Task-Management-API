FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000

CMD bash -c "celery -A app.celery_worker.celery worker --loglevel=info & uvicorn app.main:app --host 0.0.0.0 --port $PORT"