from objects.template import GeneralServer


s = GeneralServer()


@s.event("client_join")
def on_client_join(client, handle):
    print(f'{client} connected')
    handle()


@s.event("client_message")
def on_client_message(message, sender, handle):
    print(f'{sender} -> {message}')

    if message == "exit":
        s.running = False

    handle()


if __name__ == '__main__':
    s.main_loop()
