from socket import create_server, socket

from protocol import Protocol
from objects.template import Event, Handle


class ClientHandle:
    def __init__(self, connection: socket, address: tuple[str, int]):
        self.connection: socket = connection
        self.address: tuple[str, int] = address

    def __str__(self):
        return ':'.join(self.address)


class GeneralServer:
    def __init__(self):
        self.server: socket = create_server(Protocol.ADDRESS)
        self.server.settimeout(Protocol.SERVER_TIMEOUT)

        self.clients: set[ClientHandle] = set()

        # events
        self.client_message: Event = Event()
        self.server_message: Event = Event()
        self.client_join: Event = Event()
        self.client_leave: Event = Event()
        self.starting: Event = Event()
        self.closing: Event = Event()
        self.closed: Event = Event()

    def __del__(self):
        self.closed()

    def accept(self):
        try:
            connection, address = self.server.accept()

        except TimeoutError:
            return False

        new_client = ClientHandle(connection, address)
        self.clients.add(new_client)
        self.client_join(new_client, handle=Handle(), sender=self)

        return True

    def receive(self):
        pass

    def send(self):
        pass

    def main_loop(self):
        pass
