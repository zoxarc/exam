from template import GeneralClient


client = GeneralClient()


@client.event("join")
def on_join():
    print(f'joined')


if __name__ == '__main__':
    client.connect()

    while msg := input():
        client.send(msg)
        response = client.receive()

        print(response)
