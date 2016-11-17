import SocketServer
from threading import Thread

from Client import Client
from Definitions import HOST, PORT
from Plugins import get_plugins

isRunning = True
get_plugins()


class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def __init__():
    print "Server started listening on port 80."
    server = Server((HOST, PORT), Client)

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = Thread(target=server.serve_forever)

    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    server_thread.join()
    server.shutdown()
    server.server_close()

if __name__ == "__main__":
    __init__()
