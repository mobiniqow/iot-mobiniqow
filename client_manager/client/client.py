class Client:
    def __init__(self, connection):
        self.connection = connection
        self.device_id = None
        self.relay_type = None
        self.client_id = f"{connection.getpeername()[0]}:{connection.getpeername()[1]}"

    def send_message(self, message):
        self.connection.send(message)

    def set_device_id(self, device_id):
        self.device_id = device_id
