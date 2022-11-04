from objects.template import GeneralClient


client = GeneralClient()


if __name__ == '__main__':
    client.connect()

    while msg := input():
        client.send(msg)
        response = client.receive()

        print(response)

        if msg == "exit":
            break
