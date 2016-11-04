from HTTP import handle


class Client:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        print "Client added:", self.addr
        self.conn.sendall("")
        while 1:
            data = conn.recv(1024)
            if not data: break
            print "Received:", self.addr
            self.reply(data)
        print "Disconnected:", self.addr
        self.conn.close()

    def reply(self, data):
        rep = handle(data)
        self.conn.sendall(rep)
