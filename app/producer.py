import pika
from pika import exceptions
import json
from app.core.exceptions import AppException
from config import Config


class PikaClient(object):
    def __init__(self, queue: str):
        self.url = Config.RABBITMQ_SERVER
        self.queue = queue
        self.channel = None
        self.connection = None

    def connect(self):
        print(f"Connecting to server @{self.url}")
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.url)
                # pika.URLParameters(self.url)
            )
        except exceptions.AMQPConnectionError as e:
            print("Failed to connect to the broker server")
            raise AppException.BadRequest(context=e.args)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    def publish_message(self, message: list):
        self.connect()
        print("processing message!!!!")
        for index, item in enumerate(message):
            try:
                self.channel.basic_publish(
                    exchange='', routing_key=self.queue, body=json.dumps(item),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
            except exceptions.ConnectionClosed as e:
                print("no connection")
                raise AppException.BadRequest(
                    context=e.args)
        print("messages successfully queued")
        self.connection.close()
