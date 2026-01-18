#!/usr/bin/env python
import json
import pika
from InventoryService.repositories.product_repository import ProductRepository
from InventoryService.models.db_config import DbConfig

with open("consumer_is_running.txt", "a") as file:
    file.write('consumer.py is running\n')

product_repository = ProductRepository(DbConfig(
    user='postgres',
    password='postgres',
    database='Inventory',
    host='inventory-service-db'
))

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='host.docker.internal', port=7654, heartbeat=0))
channel = connection.channel()

channel.exchange_declare(exchange='payment-service-exchange', exchange_type='fanout')

result = channel.queue_declare(queue='inventory-queue', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='payment-service-exchange', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    with open("latest_received_event.json", "w") as file:
        json.dump(body.decode('utf-8'), file, indent=4)

    e = json.loads(body)
    event_type = e['type']
    order = e['payload']

    # (When InventoryService picks up a Payment-Success evnet then it should stop reserving the
    # specific product and decrease the amount of products in stock)
    if event_type == 'payment.success':
        product_repository.decrease_product_by_id(order['productId'])
    # (When InventoryService picks up the Payment-Failure event then it should stop reserving the
    # specific product.)
    else:
        product_repository.stop_reserve_product_by_id(order['productId'])



channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()