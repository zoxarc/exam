import socket
from random import randint

from sock_lib import AsyncServer

server = AsyncServer()


@server.event("client_message")
async def on_client_message(sender, message):
    await server.send_to(sender, f'{message} {randint(1, 10)}')

    if message == 'exit':
        await server.stop()


@server.event("client_connect")
async def on_client_connect(client: socket.socket):
    print(f'{client.getpeername()} connected')


@server.event("server_message")
@server.event("client_message")
async def print_messages(message, sender: socket = None, target: socket = None):
    if sender:
        print(f'{sender.getpeername()} -> {message}')

    else:
        print(f'{target.getpeername()} <- {message}')


@server.event("closing")
async def on_server_closed():
    print('server closing')


if __name__ == '__main__':
    server.main_loop()
