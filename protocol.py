from typing import Literal
from pickle import loads, dumps
from objects import Envelope


class Protocol:
    ADDRESS = ("127.0.0.1", 8080)
    SERVER_TIMEOUT = 0.1
    CLIENT_TIMEOUT = 0.1
    SIZE_BUFFER = 8
    BYTE_ORDER: Literal["little", "big"] = "little"
    RECEIVE_BUFFER = 4
    PARTIES = ["likud", "blue & white", "The work", "right"]

    @staticmethod
    def is_party(data:Envelope):
        return data in Protocol.PARTIES

    @staticmethod
    async def send_message(data, connection, loop):
        stream = dumps(data)
        size = len(stream).to_bytes(Protocol.SIZE_BUFFER, Protocol.BYTE_ORDER)

        await loop.sock_sendall(connection, size + stream)

    @staticmethod
    def get_msg(my_socket):
        size = int.from_bytes(my_socket.recv(Protocol.SIZE_BUFFER), Protocol.BYTE_ORDER)
        stream = my_socket.recv(size)
        return loads(stream)

    @staticmethod
    def is_id(id_):
        return not len(id_) != 9
