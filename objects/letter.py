from objects.note import Note


class Letter:
    def __init__(self, notes: list[Note]):
        self.notes = notes

    def status(self):
        if not self.notes:
            return "empty", None

        elif len(self.plist)>5 or len(set(self.plist)) == 1:
            return (False, null)

        else: return (True ,plist[0])

