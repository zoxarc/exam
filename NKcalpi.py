from template import GeneralClient
from objects import Envelope
from protocol import Protocol
from objects import Note

client = GeneralClient()


def get_id2():
    return input("enter your id")


def get_id():
    valid = False

    while not valid:
        try:
            id_ = int(get_id2())
            valid = True

        except TypeError:
            print("not a valid id")

    # noinspection PyUnboundLocalVariable
    return id_


def main():
    client.connect()

    id_ = get_id()  # TODO: id not part of envelope, i think they are meant to be kept locally
    for i in Protocol.PARTIES:
        print(i)

    chosen = input("choose your party: ")
    notes = [Note(chosen)]
    # noinspection GrazieInspection
    env = Envelope(notes)  # Envelopes do not contain an id, idk why, ask eli

    client.send(env)


if __name__ == '_main_':
    main()
