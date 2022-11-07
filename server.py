from objects import *


def dcount(vlist: dict, env: list[DoubleEnvelope]):
    global votes
    dvoters = [a for a in env if not a.id in list(vlist.keys())]

    for a in dvoters:
         votes.update({a.envelope.notes[0], votes.get(a.envelope.notes[0]) + 1})

def ncount(vote: envelope):
    global votes
    pass



def main():
    pass

if __name__ == "__main__":
    votes = {party: 0 for party in P.PARTIES}
    main()
