from objects.template import GeneralClient


client = GeneralClient()


@client.event("join")
def on_join():
    print(f'joined')


@client.event("client_message")
def on_client_message(message, handle):
    print(f'this was printed through an event {message}')


if __name__ == '__main__':
    client.connect()

    while msg := input():
        client.send(msg)
        response = client.receive()

        print(response)

        if msg == "exit":
            break
