import socket
from pickle import dumps

from protocol import Protocol
from objects import Note


client = socket.socket()
client.connect(Protocol.ADDRESS)


test = "test"

stream = dumps(test)

print(len(stream).to_bytes(Protocol.SIZE_BUFFER, Protocol.BYTE_ORDER))
print(stream)

client.send(len(stream).to_bytes(Protocol.SIZE_BUFFER, Protocol.BYTE_ORDER))
client.send(stream)
