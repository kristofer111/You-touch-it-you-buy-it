#!/usr/bin/env python
import json, time, uuid, pika

class Exchange:

    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='host.docker.internal', port=7654, heartbeat=0))
        self.__channel = connection.channel()

        self.__channel.exchange_declare(exchange='order-service-exchange', exchange_type='fanout')


    def send_order_created_event(self, order: dict):
        event = {
            "type": "order.created",
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time()),
            "payload": order
        }

        self.__channel.basic_publish(
            exchange='order-service-exchange',
            routing_key='',
            body=json.dumps(event),
            properties=pika.BasicProperties(content_type='application/json', delivery_mode=2)
        )
        print(f" [x] Sent order created event")

        with open("sent_events.json", "w") as file:
            json.dump(event, file, indent=4)


