from Client import Client


class Server:
    clients = []

    def __init__(self):
        print "Server started listening on port 80."

    def add(self, conn, addr):
        print "Request from:", addr
        self.clients.append(Client(conn, addr))
