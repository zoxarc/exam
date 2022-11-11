from template import GeneralClient
from objects import Envelope, DoubleEnvelope, Note
from protocol import Protocol
from clear_screen import clear


class DoubleKalpi:
    def __init__(self):
        self.client = GeneralClient()
        self.client.connect()

    def vote(self):
        id_ = ""
        while not Protocol.is_id(id_):
            id_ = input("enter your id: ")
            if id_ == "0":
                return False

        name = input("enter name: ")

        party = None
        while not Protocol.is_party(party):
            party = input(f"choose a party:\n{', '.join(Protocol.PARTIES)} ")

        if Protocol.is_party(party):
            note = Note(party)
            envelope = Envelope([note])
            double_envelope = DoubleEnvelope(envelope, name, int(id_))

            self.client.send(double_envelope)

        return True

    def run(self):
        while self.vote():
            clear()


if __name__ == '__main__':
    kalpi = DoubleKalpi()
    kalpi.run()
