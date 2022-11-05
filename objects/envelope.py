from typing import Optional

from objects import Note


class Envelope:
    def __init__(self, notes: list[Note]):
        self.notes = notes

    def status(self) -> tuple[bool, Optional[str]]:
        # TODO: this looks so bad, someone change it
        valid = 0 < len(self.notes) < 6 and len(set(note.party for note in self.notes)) == 1
        return valid, self.notes[0].party if valid else None
