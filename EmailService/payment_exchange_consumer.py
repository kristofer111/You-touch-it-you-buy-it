#!/usr/bin/env python
import json, pika
from sendgrid import Mail
from email_sender import send_email

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='host.docker.internal', port=7654, heartbeat=0))
channel = connection.channel()

channel.exchange_declare(exchange='payment-service-exchange', exchange_type='fanout')

result = channel.queue_declare(queue='email-service-payment-exchange-queue', exclusive=False)
queue_name = result.method.queue

channel.queue_bind(exchange='payment-service-exchange', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    with open("latest_received_payment_event.json", "w") as file:
        json.dump(body.decode('utf-8'), file, indent=4)

    e = json.loads(body)
    event_type = e['type']
    order = e['payload']

    if event_type == 'payment.success':
        subject = 'Order has been purchased'
        html_content = f'Order {order['id']} has been successfully purchased'

    else:
        subject = 'Order purchase failed'
        html_content = f'Order {order['id']} purchase has failed'

    send_email(Mail(
        from_email='kristofers21@ru.is',
        to_emails=['kristoferorri1@gmail.com'],  # order['buyer_email'], order['merchant_email']
        subject=subject,
        html_content=html_content
    ))




channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()