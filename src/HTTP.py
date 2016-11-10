from os.path import splitext
from re import compile

import FileManager
from Cacher import get_checksum
from Config import CRLF, ALLOW, ALLOW_ADMIN  # DocumentRoot Constant
from FileManager import get_safe
from Headers import Entity, General, Response as HResponse
from Status import STATUS_CODE

request_line = compile("(\w+) (\S+) HTTP/(\d).(\d)")
header_line = compile("([\w-]+):")
SP = " "


def get_type(data):
    data = splitext(data)[1]
    if data == ".html" or data == ".htm" or data == ".php": return "text/html"
    if data == ".png": return "image/png"
    if data == ".bmp": return "image/bmp"
    if data == ".gif": return "image/gif"
    if data == ".css" or data == ".xcss": return "text/css"
    if data == ".js": return "text/js"
    if data == ".jpeg" or data == ".jpg": return "image/jpeg"
    if data == ".json": return "application/json"
    if data == ".pdf": return "application/pdf"
    return "text/plain"


def sort_by_q(data):
    ret = []  # Make it a list instead of "None"
    for dat in data:
        ret.append(dat.split(";"))
    # Sort the list by the q value - if not q value then assume priority (1.0)
    ret.sort(key=lambda x: float(x[1][2:] if 1 < len(x) else 1.0), reverse=True)
    ret = [item[0] for item in ret]  # keep just the charsets, not qs
    return ret


class Response:
    reqline = ""

    def __init__(self, request):
        self.client = request.client
        self.major_ver = request.request['HTTP-Version'][0]
        self.minor_ver = request.request['HTTP-Version'][1]
        self.response_ver = "HTTP/{}.{}".format(self.major_ver, self.minor_ver)
        self.path = get_safe(request.request['Request-URI'])
        self.method = request.request['Method']
        self.status_code = 500  # Default to internal server error.
        if self.method == "GET":
            self.status_code = FileManager.check(self.path)

    def generate(self):
        general_header = General()
        response_header = HResponse(etag=get_checksum(self.path))
        entity_header = Entity()
        message_body = ""
        if self.method == "GET":
            if self.status_code == 404:
                response_header.retry = 120
                entity_header.c_length = 0
            elif self.status_code == 200:
                general_header.cach = "max-age=120"
                entity_header.c_type = get_type(self.path)
                entity_header.c_length = FileManager.size(self.path)
                entity_header.c_encoding = "gzip"
                response_header.retry = 120
                message_body += FileManager.open(self.path).read()
                message_body += CRLF
        elif self.method == "OPTIONS":
            self.status_code = 200
            entity_header.allow = ", ".join(ALLOW)
            if self.client.admin:
                entity_header.allow += ", ".join(ALLOW_ADMIN)
        else:
            entity_header.c_length = 0

        general_header.update()
        entity_header.update()
        response_header = response_header.generate()
        self.reqline = self.response_ver + SP + str(self.status_code) + SP + STATUS_CODE[self.status_code] + CRLF
        print "Responding:", self.reqline
        return self.reqline + general_header.header + response_header + entity_header.header + CRLF + message_body


class Request:
    enforces = {
        'charset': None,
        'encoding': None,
        'language': None,
        'authorization': None,
        'match': None,
        'unmod_since': None,
        'max_forwards': None,
    }

    def __init__(self, client, data):
        self.client = client
        self.lines = data.splitlines()
        self.message = request_line.match(self.lines[0]).groups(0)
        self.request = {  # Request Line
            'Method': self.message[0],
            'Request-URI': self.message[1],
            'HTTP-Version': [self.message[2], self.message[3]]
        }
        print "Request Received:", self.lines[0], client.addr
        for line in self.lines:
            # If it exists, use it, if we're being fooled, don't.
            if self.lines[0] == line:  # Skip the first line
                continue
            func = header_line.match(line)
            if func is not None:
                func = func.groups()[0].replace("-", "_").lower()  # Convert message to func-readable
                if self.__contains__(func):
                    self[func](line)

    # For all functions below, data is a string of the full line.
    def accept(self, data):
        return

    def accept_charset(self, data):
        data = data.replace('Accept-Charset:', ' ').strip().split(", ")
        if data.__contains__("*") or data[0] is '':
            return
        self.enforces['charset'] = sort_by_q(data)

    def accept_encoding(self, data):
        data = data.replace('Accept-Encoding:', ' ').strip().split(", ")
        if data.__contains__("*") or data[0] is '':
            return
        self.enforces['encoding'] = sort_by_q(data)

    def accept_language(self, data):
        data = data.replace('Accept-Language:', ' ').strip().split(",")
        if data.__contains__("*") or data[0] is '':
            return
        self.enforces['language'] = sort_by_q(data)

    def authorization(self, data):
        return

    def cache_control(self, data):
        return

    def connection(self, data):
        return

    def expect(self, data):
        return

    def _from(self, data):
        return

    def host(self, data):
        return

    def if_match(self, data):
        return

    def if_modified_since(self, data):
        return

    def if_none_match(self, data):
        return

    def if_range(self, data):
        return

    def if_unmodified_since(self, data):
        return

    def max_forwards(self, data):
        return

    def proxy_authorization(self, data):
        return

    def range(self, data):
        return

    def referer(self, data):
        return

    def te(self, data):
        return

    def user_agent(self, data):
        return

    def upgrade_insecure_requests(self, data):
        return

    def __getitem__(self, name):
        return getattr(self, name)

    def __contains__(self, item):
        return getattr(self, item, False)


def handle(client, data):
    request = Request(client, data)
    return Response(request)
