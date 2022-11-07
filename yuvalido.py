from template import GeneralClient

class ByeClient:
    @staticmethod
    def ByeClient():
        client = GeneralClient()
        client.send("good bye")
