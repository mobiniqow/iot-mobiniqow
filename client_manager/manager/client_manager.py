from client_manager.client.client import Client
from client_manager.manager.Singlethon import SingletonMeta


class ClientManager(metaclass=SingletonMeta):
    def __init__(self, ):
        self.clients = {}
        self.id_clients = {}

    def add_client(self, client: Client):
        # self.clients[client.device_id] = client
        self.id_clients[client.client_id] = client.device_id

    def delete_client_by_connection(self, connection):
        client_id = f"{connection.getpeername()[0]}:{connection.getpeername()[1]}"
        if client_id in self.id_clients:
            client: Client = self.id_clients[client_id]
            del self.id_clients[client_id]
            if client and client.device_id in self.clients:
                del self.clients[client.device_id]
        connection.close()

    def get_client_by_device_id(self, device_id) -> Client:
        return self.clients[device_id]

    def get_client_by_client_id(self, client_id) -> Client:
        print(client_id, client_id in self.clients)
        if client_id in self.clients:
            client = self.clients[client_id]
            return client
        return None
