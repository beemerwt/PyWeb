from os.path import isfile
from re import compile

from Cacher import get_file
from Config import DOCUMENT_ROOT, CRLF  # DocumentRoot Constant
from Headers import Entity, General, Response as HResponse
from Status import STATUS_CODE

default_files = ['index.htm', 'index.html', 'home.html', 'index.php', 'portal.php']
request_line = compile("(\w+) (\S+) HTTP/(\d).(\d)")
header_line = compile("([\w-]+):")
SP = " "


def safe_open(path):
    if path == "/":
        for name in default_files:
            if isfile(DOCUMENT_ROOT + name):
                return get_file(DOCUMENT_ROOT + name)
    path = path.replace("/", "", 1)  # Remove first occurrence of "/"
    return get_file(DOCUMENT_ROOT + path)


def check_file(path):
    if path == "/":
        for name in default_files:
            if isfile(DOCUMENT_ROOT + name):
                return 200
    path = path.replace("/", "", 1)  # Remove first occurrence of "/"
    if isfile(DOCUMENT_ROOT + path):
        return 200
    return 404


def sort_by_q(data):
    ret = []  # Make it a list instead of "None"
    for dat in data:
        ret.append(dat.split(";"))
    # Sort the list by the q value - if not q value then assume priority (1.0)
    ret.sort(key=lambda x: float(x[1][2:] if 1 < len(x) else 1.0), reverse=True)
    ret = [item[0] for item in ret]  # keep just the charsets, not qs
    return ret


class Response:
    def __init__(self, request):
        self.request = request
        self.status = request.request
        self.status_code = 500  # Default to internal server error.
        self.response_ver = "HTTP/{}.{}".format(self.status['HTTP-Version'][0], self.status['HTTP-Version'][1])
        if self.status['Method'] == "GET":
            self.status_code = check_file(self.status['Request-URI'])
        self.reqline = self.response_ver + SP + str(self.status_code) + SP + STATUS_CODE[self.status_code] + CRLF

    def generate(self):
        message = self.reqline
        if self.status['Method'] == "GET":
            if self.status_code == 404:
                message += General().generate()
                message += HResponse(retry=120).generate()
                message += Entity(clen=0).generate()
        else:
            message += General().generate()
            message += HResponse().generate()
            message += Entity(clen=0).generate()

        message += CRLF
        print "Responding:", self.reqline
        return message


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

    def __init__(self, addr, data):
        self.addr = addr
        self.lines = data.splitlines()
        self.message = request_line.match(self.lines[0]).groups(0)
        self.request = {  # Request Line
            'Method': self.message[0],
            'Request-URI': self.message[1],
            'HTTP-Version': [self.message[2], self.message[3]]
        }
        print "Request Received:", self.lines[0], addr
        for line in self.lines:
            # If it exists, use it, if we're being fooled, don't.
            if self.lines[0] == line:  # Skip the first line
                continue
            func = header_line.match(line).groups()[0].replace("-", "_").lower()  # Convert message to func-readable
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

    def __getitem__(self, name):
        return getattr(self, name)

    def __contains__(self, item):
        return getattr(self, item)


def handle(addr, data):
    request = Request(addr, data)
    return Response(request)
