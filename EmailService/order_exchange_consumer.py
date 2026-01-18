#!/usr/bin/env python
import json, pika
from sendgrid import Mail
from email_sender import send_email

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='host.docker.internal', port=7654, heartbeat=0))
channel = connection.channel()

channel.exchange_declare(exchange='order-service-exchange', exchange_type='fanout')

result = channel.queue_declare(queue='email-service-order-exchange-queue', exclusive=False)
queue_name = result.method.queue

channel.queue_bind(exchange='order-service-exchange', queue=queue_name)

print(' [*] Waiting for events. To exit press CTRL+C')

def callback(ch, method, properties, body):
    with open("latest_received_order_event.json", "w") as file:
        json.dump(body.decode('utf-8'), file, indent=4)

    e = json.loads(body)
    order = e['payload']

    # When EmailService picks up this event then we send and email to both the buyer and the merchant.
    # • The email should have the subject as "Order has been created"
    # • The Email body should include the id of the order, the name of the product, the price of the
    # order(the price of the product with the discount).

    send_email(Mail(
        from_email='kristofers21@ru.is',
        to_emails=['kristoferorri1@gmail.com'], # order['buyer_email'], order['merchant_email']
        subject='Order has been created',
        html_content=f'<strong>Order ID:</strong> {order['id']}, <strong>Product Name:</strong> {order['product_name']}, <strong>Price:</strong> {order['total_price']} V-Bucks'
        ))



channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()