from sock_lib import AsyncServer
from protocol import Protocol

from objects import *
import objects  # match throws an error when comparing types without prefix "objects."

s = AsyncServer()


def double_count(env: list[DoubleEnvelope]) -> dict:
    global votes
    double_voters = [a for a in env if a.id not in voters.keys()]  # get all voters that haven't voted via a normal calpi

    for a in double_envelopes:
         votes[a.envelope.notes[0]] += 1

    return None  # TODO: return something


def normal_count(env: Envelope):
    global votes
    votes[env.notes[0].party] += 1


@s.event("client_message")
async def on_client_message(sender, message):
    global double_envelopes
    # normal envelopes should be in a tuple containing id,name,envelope

    if message == "good bye":
        s.running = False

    match len(message):
        case 3:
            id_,name,env = message
            valid, party = env.status()
            if id_ not in voters.items() and valid:
                voters.update({id_: name})
                normal_count(env)
        case 1:
            if type(message) == str:
                s.running = False

            elif type(message) == objects.DoubleEnvelope:
                valid, party = message.envelope.status()
                if valid:
                    double_envelopes.append(message)

    print(votes)


if __name__ == "__main__":
    votes = {party: 0 for party in Protocol.PARTIES}
    voters = {}
# list of double envelopes, normal envelopes are counted while they're being recieved
# double envelopes are counted once the program is finished
    double_envelopes = []  

    s.main_loop()
