from HTTP import handle


class Client:
    def __init__(self, server, conn, addr):
        print "Connected:", addr
        self.conn = conn
        self.addr = addr
        while 1:
            data = conn.recv(1024)
            if not data: break
            self.reply(addr, data)
        print "Disconnected:", self.addr
        self.conn.close()
        server.clients[addr] = None

    def reply(self, addr, data):
        resp = handle(addr, data).generate()
        self.conn.sendall(resp)
