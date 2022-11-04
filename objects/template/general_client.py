from socket import socket
from pickle import loads, dumps

from protocol import Protocol
from objects.template import *


class GeneralClient:
    def __init__(self):
        self.client: socket = socket()

        # events
        self.client_message: Event = Event()
        self.server_message: Event = Event()
        self.join: Event = Event()
        self.closing: Event = Event()
        self.closed: Event = Event()

    def __del__(self):
        self.closed()

    def receive(self):
        size = self.client.recv(Protocol.SIZE_BUFFER)

        if size == b'':
            raise TimeoutError

        size = int.from_bytes(size, Protocol.BYTE_ORDER)
        stream = self.client.recv(size)

        message = loads(stream)
        self.server_message(message=message, handle=Handle())
        return message

    def send(self, message):
        self.client_message(message=message, handle=Handle())

        stream = dumps(message)
        size = len(stream).to_bytes(Protocol.SIZE_BUFFER, Protocol.BYTE_ORDER)
        self.client.send(size + stream)

    def connect(self):
        self.client.connect(Protocol.ADDRESS)
        self.join()

    def event(self, name: str):
        def wrapper(func):
            try:
                event = self.__getattribute__(name)

            except AttributeError:
                raise AttributeError(f'invalid event name "{name}"')

            event += func

            return func

        return wrapper

