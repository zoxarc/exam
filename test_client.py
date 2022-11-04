import socket
from pickle import dumps, loads

from protocol import Protocol


client = socket.socket()
client.connect(Protocol.ADDRESS)


while msg := input():
    stream = dumps(msg)

    client.send(len(stream).to_bytes(Protocol.SIZE_BUFFER, Protocol.BYTE_ORDER))
    client.send(stream)

    size = client.recv(Protocol.SIZE_BUFFER)
    size = int.from_bytes(size, Protocol.BYTE_ORDER)

    stream = client.recv(size)
    response = loads(stream)

    print(response)

    if msg == "exit":
        break
