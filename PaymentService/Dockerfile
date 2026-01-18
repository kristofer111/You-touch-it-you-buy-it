FROM python:3.12.1

WORKDIR /app/PaymentService

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "consumer.py"]


