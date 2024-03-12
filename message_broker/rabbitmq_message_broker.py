import json
import threading

import pika

from client_manager.manager.client_manager import ClientManager
from message.encryption.decoder.rsa_decoder import RSADecoder


class RabbitMQMessageBroker(threading.Thread):

    def send_message_from_device(self, client_id, content):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='send_message_from_device')
        message = {
            'client_id': client_id,
            'message': str(content),
        }
        message = self.serialize_object(message)
        channel.basic_publish(exchange='', routing_key='send_message_from_device', body=message)
        connection.close()

    def __init__(self, host, queue_name, callback):
        threading.Thread.__init__(self)
        self.host = host
        self.client_manager = ClientManager()
        self.queue_name = queue_name
        self.callback = callback

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='send_message_from_server', )
        channel.basic_consume('send_message_from_server', self.message_from_server, )
        channel.start_consuming()

    def server_to_device_data(self, channel, method, properties, body):
        result = body.decode()
        result = json.loads(result)
        # self.client_manager.get_client_by_client_id(result['client_id']).send_message(result['message'])
        # self.callback(result['client_id'], result['message'])

        if self.client_manager.get_client_by_client_id(result['client_id']):
            self.client_manager.get_client_by_client_id(result['client_id']).send_message(result['message'])

        # print(f"Received message from {result['client_id']}: {result['message']}")

    def message_from_server(self, channel, method, properties, body):
        print("23232323")
        print(f"body{body}")
        message_encoder = RSADecoder()
        content = message_encoder.decode(body)
        print(f'content {content}')

    def serialize_object(self, obj):
        return json.dumps(obj)
