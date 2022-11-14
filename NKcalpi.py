from template import GeneralClient
from objects import Envelope
from protocol import Protocol
from objects import Note
from time import sleep
from clear_screen import clear

client = GeneralClient()


def get_id():
    valid = False

    while not valid:
        id_ = input("enter your id: ")
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
    votersdic = {123456789: "zohar", 987654321 : "yuval", 192837465 : "nerya", 918273645 : "shahar", 918273646 : "idotheking",918273649 : "yoavtheshovav"}
    client.connect()
    while len(votersdic) != 0:
        while True:
            id_ = get_id()
            name = input("enter your name: ")
            if (id_,name) in votersdic.items():
                votersdic.pop(id_)
                break
            else:
                print("Sorry! You're not on the voter list")
        for i in Protocol.PARTIES:
            print(i)

        chosen = input("choose your party: ")
        notes = [Note(chosen)]
        # noinspection GrazieInspection
        env = Envelope(notes)  # Envelopes do not contain an id, idk why, ask eli
        client.send((id_,name,env))
        clear()
        sleep(0.5)





if __name__ == '__main__':

    main()
