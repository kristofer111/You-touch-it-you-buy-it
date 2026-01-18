#!/usr/bin/env python
import json, time, uuid, pika
from card_validator import is_payment_valid
from exchange import Exchange
from repository import Repository

exchange = Exchange()
repository = Repository()


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='host.docker.internal', port=7654, heartbeat=0))
channel = connection.channel()

channel.exchange_declare(exchange='order-service-exchange', exchange_type='fanout')

result = channel.queue_declare(queue='payment-service-queue', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='order-service-exchange', queue=queue_name)

print(' [*] Waiting for events. To exit press CTRL+C')

def callback(ch, method, properties, body):
    with open("latest_received_event.json", "w") as file:
        json.dump(body.decode('utf-8'), file, indent=4)

    e = json.loads(body)
    order = e['payload']

    # validate the credit card information
    payment_result = 'payment.success' if is_payment_valid(order['creditCard']) else 'payment.failure'

    event = {
        'type': payment_result,
        'id': str(uuid.uuid4()),
        'timestamp': int(time.time()),
        'payload': order
    }

    # if valid then send out a payment success event else send out a payment failed event.
    exchange.send_payment_event(event)

    # store the payment results in db. What needs to be stored is the order id and the payment result.
    repository.create_payment_result(order['id'], payment_result)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()