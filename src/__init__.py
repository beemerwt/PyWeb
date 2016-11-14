import socket

from Definitions import HOST, PORT
from Plugins import get_plugins
from Server import Server

isRunning = True
get_plugins()


def __init__():
    while isRunning:
        sock = socket.socket()
        sock.bind((HOST, PORT))
        sock.listen(0)
        conn, addr = sock.accept()
        server.add(conn, addr)


if __name__ == "__main__":
    server = Server()
    __init__()
