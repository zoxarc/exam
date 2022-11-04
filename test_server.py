from objects.template import *


s = GeneralServer()


@s.event("client_join")
def on_client_join(client, handle):
    print(f'{client} connected')
    handle()


@s.event("client_message")
def on_client_message(message: str, sender: ClientHandle, handle: Handle):
    print(f'{sender} -> {message}')

    sender.send(message)

    if message == "exit":
        s.running = False

    handle()


@s.event("server_message")
def on_server_message(message: str, target: ClientHandle, handle: Handle):
    print(f"{target} <- {message}")
    handle()


if __name__ == '__main__':
    s.main_loop()
