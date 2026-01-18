#!/usr/bin/env python
import json, pika

class Exchange:

    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='host.docker.internal', port=7654, heartbeat=0))
        self.__channel = connection.channel()

        self.__channel.exchange_declare(exchange='payment-service-exchange', exchange_type='fanout')


    def send_payment_event(self, event: dict):

        self.__channel.basic_publish(
            exchange='payment-service-exchange', # sending to order-service-exchange here creates an infinite loop
            routing_key='',
            body=json.dumps(event),
            properties=pika.BasicProperties(content_type='application/json', delivery_mode=2)
        )
        print(f" [x] Sent payment event")

        with open("sent_events.json", "w") as file:
            json.dump(event, file, indent=4)