from __future__ import annotations
from typing import Literal
from socket import create_server, socket
from pickle import dumps, loads

from protocol import Protocol
from template import Event, Handle
from template.type_hints import func


class ClientHandle:
    def __init__(self, connection: socket, address: tuple[str, int], owner: GeneralServer):
        self.connection: socket = connection
        self.address: tuple[str, int] = address
        self.owner: GeneralServer = owner

        self.connection.settimeout(Protocol.SERVER_TIMEOUT)

    def __str__(self):
        return ':'.join(map(str, self.address))

    def receive(self):
        size = self.connection.recv(Protocol.SIZE_BUFFER)

        while size.endswith(b'ping'):
            size = self.connection.recv(Protocol.SIZE_BUFFER)

        if size == b'':
            raise TimeoutError

        size = int.from_bytes(size, Protocol.BYTE_ORDER)

        stream = []
        while size > 0:
            stream.append(self.connection.recv(Protocol.RECEIVE_BUFFER))
            size -= Protocol.RECEIVE_BUFFER

        return loads(b''.join(stream))

    def send(self, message):
        self.owner.server_message(message=message, target=self, handle=Handle())

        stream = dumps(message)
        size = len(stream).to_bytes(Protocol.SIZE_BUFFER, Protocol.BYTE_ORDER)
        self.connection.send(size + stream)

    def ping(self):
        stream: bytes = b'ping'.zfill(Protocol.SIZE_BUFFER)
        self.connection.send(stream)


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
        self.closed(sender=self, handled=Handle())

    def accept(self):
        try:
            connection, address = self.server.accept()

        except TimeoutError:
            return False

        new_client = ClientHandle(connection, address, self)
        self.clients.add(new_client)
        self.client_join(client=new_client, handle=Handle())

        return True

    def receive_all(self):
        disconnected_clients = set()

        for client in self.clients:
            try:
                message = client.receive()

            except TimeoutError:
                continue

            except ConnectionResetError:
                disconnected_clients.add(client)
                self.client_leave(client=client, handle=Handle())
                continue

            self.client_message(message=message, sender=client, handle=Handle())

        self.clients = self.clients.difference(disconnected_clients)

    def ping_all(self):
        disconnected_clients = set()

        for client in self.clients:
            try:
                client.ping()

            except (BrokenPipeError, ConnectionResetError):
                disconnected_clients.add(client)
                self.client_leave(client=client, handle=Handle())
                continue

        self.clients = self.clients.difference(disconnected_clients)

    def main_loop(self):
        self.starting(handled=Handle())

        while self.running:
            self.accept()
            self.receive_all()
            self.ping_all()

        self.closing(handled=Handle())

    def event(self, name: Literal[
        "client_message", "server_message", "client_join", "client_leave", "starting", "closing", "closed"
    ]) -> func:
        def wrapper(f):
            try:
                event = self.__getattribute__(name)

            except AttributeError:
                raise AttributeError(f'invalid event name "{name}"')

            event += f

            return f

        return wrapper
