FROM python:3.12.1

WORKDIR /app/EmailService

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python order_exchange_consumer.py & python payment_exchange_consumer.py"]