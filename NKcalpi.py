from template import GeneralClient
from objects import Envelope
from protocol import Protocol
from objects import Note


client = GeneralClient()


@client.event("join")
def on_join():
    print(f'joined')

def getId2():
    return input("enter your id")

def getId():
    valid = True
    while valid:
        valid = True
        try:
            id_ = int(getId2())
        except TypeError:
            print("not a valid id")
            valid = False
    return id_

def main():
    client.connect()

    id_ = getId()
    for i in Protocol.MIFLAGOT:
        print(i)

    chosen = input("choose your miflaga: ")
    notes = [Note(chosen)]
    env = Envelope(id_, notes)

    while msg := input():
        client.send(env)
        response = client.receive()

        print(response)

if _name_ == '_main_':
    main()
