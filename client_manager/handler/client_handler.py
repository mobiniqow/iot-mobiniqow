import socketserver

from client_manager.client.client import Client
from client_manager.manager.client_manager import ClientManager
from message_broker.rabbitmq_message_broker import RabbitMQMessageBroker


class ClientHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):

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
            ClientManager().add_client(client)
            self.message_broker.send_message_from_device(client.id,data.decode())

    def finish(self) -> None:
        ClientManager().delete_client_by_connection(self.request)
        self.request.close()

    def listen_to_message(self, client_id, message):
        print(f"Received message from {client_id}: {message}")
