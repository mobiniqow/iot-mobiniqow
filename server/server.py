import socketserver

from client_manager.handler.client_handler import ClientHandler


class TCPServer:
    def __init__(self, port):
        self.httpd = socketserver.ThreadingTCPServer(('localhost', port), ClientHandler, False)
        self.httpd.allow_reuse_address = True
        self.httpd.server_bind()
        self.httpd.server_activate()

    def start(self):
        self.httpd.serve_forever()
