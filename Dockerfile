FROM python:3.12-alpine

WORKDIR /app

COPY .env .env
COPY requirements.txt requirements.txt
COPY pastor pastor

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "pastor.main:app", "--host=0.0.0.0", "--port=8000"]
