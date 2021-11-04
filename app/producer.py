import pika
from pika import exceptions
import json
from app.core.exceptions import AppException


class PikaClient(object):
    def __init__(self, url: str, queue: str):
        self.url = url
        self.queue = queue
        self.channel = None
        self.connection = None

    def connect(self):
        print(f"Connecting to server @{self.url}")
        try:
            self.connection = pika.BlockingConnection(
                # pika.ConnectionParameters(host=self.url)
                pika.URLParameters(self.url)
            )
        except exceptions.AMQPConnectionError:
            print("Failed to connect to the broker server")
            raise AppException.BadRequest(context="error contacting server")
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
            except exceptions.ConnectionClosed:
                print("no connection")
                raise AppException.BadRequest(
                    context="error contacting server")
        print("messages successfully queued")
        self.connection.close()

#
# def create_email_queue(email_parameters: dict):
#     email_parameters["service_channel"] = "email"
#     try:
#         connection = pika.BlockingConnection(pika.ConnectionParameters
#                                              (host="localhost"))
#     except exceptions.AMQPConnectionError:
#         print("Failed to connect to the broker server")
#         return
#
#     channel = connection.channel()
#     channel.queue_declare(queue="notification", durable=True)
#     channel.basic_publish(
#         exchange="",
#         routing_key="notification",
#         body=json.dumps(email_parameters),
#         properties=pika.BasicProperties(
#             delivery_mode=2,
#         )
#     )
#     print("email queue sent")
#     connection.close()
#
#
# def create_sms_queue(sms_parameters: dict):
#     sms_parameters["service_channel"] = "sms"
#     try:
#         connection = pika.BlockingConnection(pika.ConnectionParameters
#                                              (host="localhost"))
#     except exceptions.AMQPConnectionError:
#         print("Failed to connect to the broker server")
#         return
#
#     channel = connection.channel()
#     channel.queue_declare(queue="notification", durable=True)
#     channel.basic_publish(
#         exchange="",
#         routing_key="notification",
#         body=json.dumps(sms_parameters),
#         properties=pika.BasicProperties(
#             delivery_mode=2
#         )
#     )
#     print("sms queeue sent")
#     connection.close()
#
#
# # import pika
# #
# class PikaClient:
#     def __init__(self, url=None, queue=None):
#         self.connection = None
#         self.channel = None
#         self.queue = queue
#         self.url = url
#
#     def __enter__(self):
#         print(f"Connecting to broker server @{self.url}")
#         try:
#             self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.url))
#         except exceptions.AMQPConnectionError:
#             print(f"error contacting broker server @{self.url}")
#             return
#         else:
#             print("Connection successful!!")
#         self.channel = self.connection.channel()
#         self.channel.queue_declare(queue=self.queue)
#         # self.connection = connection
#         # self.channel = channel
#         return self
#
#     def __exit__(self, type, value, traceback):
#         print(f"Closing connection to broker server @{self.url}")
#         self.connection.close()
#
#     def publish_message(self, message: list):
#         print("Creating queue on broker")
#         for index, item in enumerate(message):
#             print(message[index])
#         # message_body = json.dumps(message)
#             self.channel.basic_publish(
#                 exchange='', routing_key=self.queue, body=json.dumps(item),
#                 properties=pika.BasicProperties(delivery_mode=2)
#             )
#         print("queue successful!!!")
#
#     # def messageSent(self, msgStr):
#     #     self.channel.basic_publish(exchange='', routing_key='myqueue', body=msgStr)
# #
# # and then when you want to send a message:
# #
# # with PikaClient() as pClient:
# #     pClient.messageSent("my message")