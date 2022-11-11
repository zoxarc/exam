from template import GeneralClient
from objects import Envelope, DoubleEnvelope, Note
from protocol import Protocol
from clear_screen import clear


class DoubleKalpi:
    def __init__(self):
        self.client = GeneralClient()
        self.client.connect()

    def vote(self):
        party = None
        while not Protocol.is_party(party):
            party = input(f"choose a party:\n{', '.join(Protocol.PARTIES)} ")

        id_ = None
        while not Protocol.is_id(id_):
            id_ = input("enter your id: ")

        if Protocol.is_party(party):
            note = Note(party)
            envelope = Envelope([note])
            double_envelope = DoubleEnvelope(envelope, input("enter name: "), int(id_))

            self.client.send(double_envelope)

    def run(self):
        while True:
            self.vote()
            clear()


if __name__ == '__main__':
    kalpi = DoubleKalpi()
    kalpi.run()
    print(4)
