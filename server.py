from sock_lib import AsyncServer
from protocol import Protocol

from objects import *
import objects  # match throws an error when comparing types without prefix "objects."

s = AsyncServer()


def double_count(env: list[DoubleEnvelope]) -> dict:
    global votes
    double_voters = [a for a in env if a.id not in voters.keys()]  # TODO: what is this for?

    for a in double_voters:
         votes[a.envelope.notes[0]] += 1


def normal_count(env: Envelope):
    global votes
    votes[env.notes[0]] += 1


@s.event("client_message")
async def on_client_message(sender, message):
    match type(message):
        case objects.Envelope:
            if message.id not in voters.items():
                voters.update({message.id: message.name})

            # TODO: non double envelopes dont contain name and id,
            #  need to verify how they work first

        case objects.DoubleEnvelope:
            # TODO: this

            pass


if __name__ == "__main__":
    votes = {party: 0 for party in Protocol.PARTIES}
    voters = {}
    double_voters = {}  # TODO: double voters? (originally ddict) if so why redefine at double_count?

    s.main_loop()
