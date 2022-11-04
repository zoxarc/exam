class paper:
    def __init__(self, competitor: str):
        self.com = competitor

class letter:
    def __init__(self, paperlist: paper):
        self.plist = paperlist
    def status(self):
        if not self.plist:
            return (null, null)
        elif len(self.plist)>5 or len(set(self.plist)) == 1:
            return (False, null)
        else: return (True ,plist[0])

class dletter:
    def __init__(self, letter, name, id):
        self.letter = letter
        self.name = name
        self.id = id
