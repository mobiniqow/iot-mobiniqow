from client_manager.client.client import Client
from client_manager.manager.Singlethon import SingletonMeta


class ClientManager(metaclass=SingletonMeta):
    def __init__(self, ):
        self.device_ids = {}
        self.client_ids = {}

    def add_client(self, client: Client):
        # self.clients[client.device_id] = client
        self.client_ids[client.client_id] = client

    def delete_client_by_connection(self, connection):
        client_id = f"{connection.getpeername()[0]}:{connection.getpeername()[1]}"
        if client_id in self.client_ids:
            client: Client = self.client_ids[client_id]
            del self.client_ids[client_id]
            if client and client.device_id in self.device_ids:
                del self.device_ids[client.device_id]
        connection.close()

    def get_client_by_device_id(self, device_id) -> Client:
        return self.device_ids[device_id]

    def get_client_by_client_id(self, client_id) -> Client:
        if client_id in self.client_ids:
            client = self.client_ids[client_id]
            return client
        return None
