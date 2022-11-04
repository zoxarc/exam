import socket
from pickle import dumps

from protocol import Protocol


client = socket.socket()
client.connect(Protocol.ADDRESS)


while msg := input():
    stream = dumps(msg)

    client.send(len(stream).to_bytes(Protocol.SIZE_BUFFER, Protocol.BYTE_ORDER))
    client.send(stream)

    if msg == "exit":
        break
