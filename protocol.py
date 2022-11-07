from typing import Literal
from pickle import loads, dumps
from objects import Envelope
import socket


class Protocol:
    ADDRESS = ("127.0.0.1", 8080)
    SERVER_TIMEOUT = 0.1
    CLIENT_TIMEOUT = 0.1
    SIZE_BUFFER = 8
    BYTE_ORDER: Literal["little", "big"] = "little"
    RECEIVE_BUFFER = 4
    PARTIES = ["likud", "blue & white", "The work", "right"]

    @staticmethod
    def IsParty(data:Envelope):
        return data in Protocol.PARTIES

    @staticmethod
    def send_msg(my_socket, data):
        stream = dumps(data)
        size = len(stream)
        size = int.to_bytes(size, Protocol.SIZE_BUFFER, Protocol.BYTE_ORDER)

        my_socket.send(size + stream)

    @staticmethod
    def get_msg(my_socket):
        size = int.from_bytes(my_socket.recv(Protocol.SIZE_BUFFER), Protocol.BYTE_ORDER)
        stream = my_socket.recv(size)
        return loads(stream)
