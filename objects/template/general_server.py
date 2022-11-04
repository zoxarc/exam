from __future__ import annotations
from socket import create_server, socket
from pickle import dumps, loads

from protocol import Protocol
from objects.template import Event, Handle


class ClientHandle:
    def __init__(self, connection: socket, address: tuple[str, int]):
        self.connection: socket = connection
        self.address: tuple[str, int] = address

    def __str__(self):
        return ':'.join(self.address)

    def receive(self):
        size = self.connection.recv(Protocol.SIZE_BUFFER)
        size = int.from_bytes(size, Protocol.BYTE_ORDER)
        stream = self.connection.recv(size)
        return loads(stream)

    def send(self, data, sender: GeneralServer):
        sender.server_message(data, sender=self, handled=Handle())

        stream = dumps(data)
        size = len(stream).to_bytes(Protocol.SIZE_BUFFER, Protocol.BYTE_ORDER)
        self.connection.send(size + stream)


class GeneralServer:
    def __init__(self):
        self.server: socket = create_server(Protocol.ADDRESS)
        self.server.settimeout(Protocol.SERVER_TIMEOUT)
        self.server.listen()

        self.clients: set[ClientHandle] = set()
        self.running = True

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

    def receive_all(self):
        for client in self.clients:
            try:
                data = client.receive()

            except TimeoutError:
                continue

            self.client_message(data, handled=Handle(), sender=self)

    def main_loop(self):
        while self.running:
            self.accept()
            self.receive_all()

        self.closing(sender=self, handled=Handle())
