from objects import Envelope


class DoubleEnvelope:
    def __init__(self, letter: Envelope, name: str, id_: int):
        self.letter = letter
        self.name = name
        self.id = id_
