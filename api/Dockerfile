FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app
# COPY .env . # Commented out to bypass missing .env file error

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]