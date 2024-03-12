import datetime
import socketserver

from client_manager.client.client import Client
from client_manager.manager.client_manager import ClientManager
from message.encryption.encoder.rsa_encoder import RSAEncoder
from message.message_generator import MessageGenerator
from message.message_template.rabbie_template import RabbieTemplate
from message_broker.rabbitmq_message_broker import RabbitMQMessageBroker


class ClientHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        rabbie_template = RabbieTemplate()
        encoder = RSAEncoder()
        self.message_generator = MessageGenerator(template=rabbie_template, encoder=encoder)
        self.message_broker = RabbitMQMessageBroker(host='localhost', queue_name='device_message',
                                                    callback=self.listen_to_message)
        self.message_broker.start()
        super().__init__(request, client_address, server)

    def setup(self) -> None:
        pass

    def handle(self) -> None:
        conn = self.request
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            client = Client(conn)
            # ClientManager().add_client(client)
            # ClientManager().add_client(client)
            encoded_message = self.message_generator.generate(message_data=data.decode('windows-1252'), client_id=client.client_id,
                                                              message_date=datetime.datetime.now())
            self.message_broker.send_message_from_device(client.client_id, encoded_message)

    def finish(self) -> None:
        ClientManager().delete_client_by_connection(self.request)
        self.request.close()

    def listen_to_message(self, client_id, message):
        print(f"Received message from {client_id}:{message}")
