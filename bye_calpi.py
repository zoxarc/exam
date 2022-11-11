from template import GeneralClient
from time import sleep


class ByeClient:
    def __init__(self):
        self.client = GeneralClient()
        self.client.connect()

    def bye_client(self):
        self.client.send("good bye")


if __name__ == '__main__':
    client = ByeClient()
    client.bye_client()
    sleep(10)

