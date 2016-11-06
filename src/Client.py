from HTTP import handle


def reply(data):
    return handle(data).generate().replace("\n", "\r\n")


class Client:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        print "Client added:", self.addr
        self.conn.sendall("")
        while 1:
            data = conn.recv(1024)
            if not data: break
            print "Data received:", data
            p = reply(data)
            print p

        print "Disconnected:", self.addr
        self.conn.close()
