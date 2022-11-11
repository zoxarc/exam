import asyncio
from asyncio import get_event_loop, ensure_future, sleep, gather
from socket import create_server, socket
from pickle import dumps, loads
from select import select

from protocol import Protocol


class AsyncServer:
    class AsyncEvent:
        def __init__(self):
            self.delegate = set()

        def __add__(self, other):
            self.delegate.add(other)
            return self

        def __sub__(self, other):
            self.delegate.remove(other)
            return self

        def __call__(self, *args, **kwargs):
            for f in self.delegate:
                ensure_future(f(*args, **kwargs))

    def __init__(self):
        self.server: socket = create_server(Protocol.ADDRESS)
        self.server.settimeout(Protocol.SERVER_TIMEOUT)
        self.server.listen()

        self.running = True

        self.potential_readers = {self.server}
        self.potential_writers = set()
        self.potential_errs = set()
        self.disconnected = set()

        self.loop = get_event_loop()

        self.client_message = AsyncServer.AsyncEvent()
        self.server_message = AsyncServer.AsyncEvent()
        self.client_connect = AsyncServer.AsyncEvent()
        self.client_disconnect = AsyncServer.AsyncEvent()
        self.ready = AsyncServer.AsyncEvent()
        self.closing = AsyncServer.AsyncEvent()
        self.closed = AsyncServer.AsyncEvent()

    async def send_to(self, connection: socket, message):
        await Protocol.send_message(message, connection, self.loop)
        self.server_message(target=connection, message=message)

    async def receive_from(self, connection):
        if connection is self.server:
            return

        try:
            size = connection.recv(Protocol.SIZE_BUFFER)

        except (ConnectionAbortedError, ConnectionResetError, TimeoutError, OSError):
            return

        if size == b'':
            return

        size = int.from_bytes(size, Protocol.BYTE_ORDER)

        stream = connection.recv(size)
        message = loads(stream)

        self.client_message(sender=connection, message=message)
        return message

    async def ping(self, connection):
        try:
            await self.loop.sock_sendall(connection, b'ping')

        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            self.disconnected.add(connection)
            ensure_future(self.remove_disconnected())
            self.client_disconnect(connection)

    async def remove_disconnected(self):
        self.potential_errs = self.potential_errs.difference(self.disconnected)
        self.potential_readers = self.potential_readers.difference(self.disconnected)
        self.potential_writers = self.potential_writers.difference(self.disconnected)

        self.disconnected.clear()

    async def __ping_loop(self):
        while self.running:
            _, ready, _ = select(
                self.potential_readers,
                self.potential_writers,
                self.potential_errs,
                Protocol.SERVER_TIMEOUT
            )

            for connection in ready:
                ensure_future(self.ping(connection))

            await sleep(0.1)

    async def __main_task(self):
        task1 = self.__ping_loop()
        task2 = self.__accept_loop()
        task3 = self.__receive_loop()

        task1 = asyncio.create_task(task1)
        task2 = asyncio.create_task(task2)
        task3 = asyncio.create_task(task3)

        while self.running:
            await sleep(1)

        await gather(task1, task2, task3)

    async def __receive_loop(self):
        while self.running:
            ready, _, _ = select(
                self.potential_readers,
                self.potential_writers,
                self.potential_errs,
                Protocol.SERVER_TIMEOUT
            )

            for connection in ready:
                ensure_future(self.receive_from(connection))

            await sleep(0.1)

    async def __accept_loop(self):
        while self.running:
            ready, _, _ = select(
                self.potential_readers,
                self.potential_writers,
                self.potential_errs,
                Protocol.SERVER_TIMEOUT
            )

            if self.server in ready:
                connection, address = await self.loop.sock_accept(self.server)
                connection.settimeout(Protocol.SERVER_TIMEOUT)

                self.potential_writers.add(connection)
                self.potential_readers.add(connection)

                self.client_connect(client=connection)

            await sleep(0.1)

    def main_loop(self):
        main_task = self.__main_task()
        self.loop.run_until_complete(main_task)

        self.closed()
        self.loop.close()

    async def stop(self):
        self.closing()
        self.running = False

    def event(self, name):
        def wrapper(f):
            try:
                event = self.__getattribute__(name)

            except AttributeError:
                raise AttributeError(f'invalid event name "{name}"')

            event += f

            return f

        return wrapper
