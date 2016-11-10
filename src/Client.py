from Config import ADMIN_LIST
from HTTP import handle


class Client:
    admin = False

    def __init__(self, server, conn, addr):
        print "Connected:", addr
        if ADMIN_LIST.__contains__(addr[0]):
            print addr, "is Admin."
            self.admin = True
        self.conn = conn
        self.addr = addr
        while 1:
            data = conn.recv(1024)
            if not data: break
            self.reply(data)
        print "Disconnected:", self.addr
        self.conn.close()
        server.clients[addr] = None

    def reply(self, data):
        resp = handle(self, data).generate()
        self.conn.sendall(resp)
