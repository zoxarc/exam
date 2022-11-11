from template import GeneralClient
from objects import Envelope
from protocol import Protocol
from objects import Note
from time import sleep

client = GeneralClient()


def get_id():
    valid = False

    while not valid:
        id_ = input("enter your id")
        try:
            if len(id_) != 9:

                raise TypeError
            id_ = int(id_)
            valid = True

        except TypeError:
            print("not a valid id")

    # noinspection PyUnboundLocalVariable
    return id_


def main():
    client.connect()

    id_ = get_id()  
    name = input("enter your name")
    for i in Protocol.PARTIES:
        print(i)

    chosen = input("choose your party: ")
    notes = [Note(chosen)]
    # noinspection GrazieInspection
    env = Envelope(notes)  # Envelopes do not contain an id, idk why, ask eli

    client.send((id_,name,env))
    sleep(0.5)


if __name__ == '__main__':
    main()
