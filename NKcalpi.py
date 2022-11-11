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
            if len(id_ != 9):
                raise TypeError
            id_ = int(get_id2())
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


if __name__ == '__main__':
    main()
