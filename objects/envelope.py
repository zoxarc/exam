from typing import Optional

from objects import Note


class Envelope:
    def __init__(self, notes: list[Note]):
        self.notes: list[Note] = notes

    def status(self) -> tuple[bool, Optional[str]]:
        parties = list(note.party for note in self.notes)
        valid = 0 < len(self.notes) < 6 and len(parties) == 1

        return valid, parties[0] if valid else None
