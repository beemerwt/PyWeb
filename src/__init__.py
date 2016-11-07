import socket

from Cacher import cache_all
from Server import Server

HOST = ''
PORT = 80
isRunning = True
checksums = []


def __init__():
    cache_all()
    while isRunning:
        sock = socket.socket()
        sock.bind((HOST, PORT))
        sock.listen(0)
        conn, addr = sock.accept()
        server.add(conn, addr)


server = Server()
__init__()
