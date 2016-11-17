from SocketServer import BaseRequestHandler
from threading import current_thread

from Config import ADMIN_LIST, LOG_ON_CONNECT, LOG_ON_DISCONNECT
from Request import Request

clients = {}


class Client(BaseRequestHandler):
    admin = False
    cur_thread = None

    def setup(self):
        if ADMIN_LIST.__contains__(self.client_address[0]):
            self.admin = True

        if LOG_ON_CONNECT:
            print "Connected:", self.client_address, ("is Admin" if self.admin else "")

        self.cur_thread = current_thread()
        clients[self.cur_thread] = self

    def handle(self):
        data = self.request.recv(1024)
        self.reply(data)

    def finish(self):
        if LOG_ON_DISCONNECT:
            print "Disconnected:", self.client_address, "\n"
        clients[self.cur_thread] = None

    def reply(self, data):
        resp = Request(self, data).respond().generate()
        self.request.sendall(resp)
