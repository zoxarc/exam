from objects import *
from protocol import Protocol as P
from sock_lib import GeneralServer
s = GeneralServer()


def dcount(env: list[DoubleEnvelope]) -> dict:
    global votes
    dvoters = [a for a in env if a.id not in list(vlist.keys())]

    for a in dvoters:
         votes.update({a.envelope.notes[0], votes.get(a.envelope.notes[0]) + 1})


def ncount(env: Envelope):
    global votes
    votes.update({env.notes[0], votes.get(env.notes[0]) + 1})


@s.event("client_message")
async def on_client_message(sender, message):
    match type(message):
        case Envelope:
            if message.id not in vdict:
                vdict.update(message.id: message.name)
        case DoubleEnvelope:
            ddict.update(message)




def main():
    s.main_loop()

if __name__ == "__main__":
    votes = {party: 0 for party in P.PARTIES}
    vdict = {}
    ddict = {}
    main()

