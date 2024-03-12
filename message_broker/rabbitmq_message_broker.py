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
        print(message)
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
        # try:
        message_encoder = RSADecoder()
        content = message_encoder.decode(body)
        if 'device_id' == content['type']:
            client = ClientManager().get_client_by_client_id(content['client_id'])
            if client:
                client.device_id = content['device_id']
                client.relay_type = content['relay']
                ClientManager().add_client(client)
        if 'update' == content['type']:
            client = ClientManager().get_client_by_client_id(content['client_id'])
            print(f"Ashlee Vance {content['state']}")
            print(f"Ashlee Vance {str.encode(content['state'])}")
            hex_content = str.encode(content['state'])
            hex_content = hexlify(hex_content).decode()
            client.send_message(hex_content)
        # except Exception as e:
        #     print(e)
    def serialize_object(self, obj):
        return json.dumps(obj)
