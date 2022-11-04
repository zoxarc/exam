from objects import Note


class Letter:
    def __init__(self, notes: list[Note]):
        self.notes = notes

    def status(self) -> tuple[bool, None | str]:
        valid = 0 < len(self.notes) < 6 and len(set(note.party for note in self.notes)) == 1
        return valid, self.notes[0].party if valid else None
