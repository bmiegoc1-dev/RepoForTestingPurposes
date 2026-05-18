FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cart_project/ ./cart_project/

WORKDIR /app/cart_project

EXPOSE 5000

CMD ["python", "main.py"]
