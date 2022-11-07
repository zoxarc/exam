from objects import *
from protocol import Protocol as P


def dcount(vlist: dict, env: list[DoubleEnvelope]) -> dict:
    global votes
    dvoters = [a for a in env if a.id not in list(vlist.keys())]

    for a in dvoters:
         votes.update({a.envelope.notes[0], votes.get(a.envelope.notes[0]) + 1})
    return votes


#def ncount()


def main():
    pass

if __name__ == "__main__":
    votes = {party: 0 for party in P.PARTIES}
    main()

