from socket import create_server, socket

from protocol import Protocol
from objects.template import Event


class ClientHandle:
    def __init__(self, connection: socket, address: tuple[str, int]):
        # type hints
        self.connection: socket
        self.address: tuple[str, int]

        #
        self.connection = connection
        self.address = address


class GeneralServer:
    def __init__(self):
        # type hints

        self.server: socket
        self.clients: set[ClientHandle]

        self.client_message: Event
        self.starting: Event
        self.closing: Event
        self.closed: Event

        #
        self.server = create_server(Protocol.ADDRESS)
        self.server.settimeout(Protocol.SERVER_TIMEOUT)

        self.clients = set()

        # events
        self.client_message = Event()
        self.starting = Event()
        self.closing = Event()
        self.closed = Event()

    def __del__(self):
        self.closed()

    def accept(self):
        pass

    def receive(self):
        pass

    def send(self):
        pass

    def main_loop(self):
        pass
