from objects import Envelope


class DoubleEnvelope:
    def __init__(self, envelope: Envelope, name: str, id_: int):
        self.envelope = envelope
        self.name = name
        self.id = id_

    def __len__(self):
        return 1
