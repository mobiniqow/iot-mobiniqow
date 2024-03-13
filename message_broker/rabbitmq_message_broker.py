import json
import threading
from binascii import hexlify

import pika

from client_manager.manager.client_manager import ClientManager
from message.encryption.decoder.rsa_decoder import RSADecoder


class RabbitMQMessageBroker(threading.Thread):

    def send_message_from_device(self, client_id, content):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='send_message_from_device')
        client = self.client_manager.get_client_by_client_id(client_id)

        message = {
            'client_id': client_id,
            'relay': client.relay_type,
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

    def message_from_server(self, channel, method, properties, body):
        try:
            message_encoder = RSADecoder()
            content = message_encoder.decode(body)

            if content['type'] == 'device_id':
                client = ClientManager().get_client_by_client_id(content['client_id'])
                if client:
                    client.device_id = content['device_id']
                    client.relay_type = content['relay']
                    ClientManager().add_client(client)

            if content['type'] == 'update':
                client = ClientManager().get_client_by_client_id(content['client_id'])
                state = content['state']
                hex_content = str.encode(state)
                hex_content = hexlify(hex_content).decode()
                client.send_message(hex_content.encode())

            if content['type'] == 'fetch':
                client = ClientManager().get_client_by_client_id(content['client_id'])
                state = content['state']
                hex_content = str.encode(state)
                hex_content = hexlify(hex_content).decode()
                client.send_message(hex_content.encode())

        except Exception as e:
            print(e)

    def serialize_object(self, obj):
        return json.dumps(obj)
