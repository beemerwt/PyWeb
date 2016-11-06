from os.path import isfile
from re import compile

from Cacher import get_file
from Config import DOCUMENT_ROOT  # DocumentRoot Constant
from Headers import Response as HResponse
from Headers import StatusLine, General, Entity

default_files = ['index.htm', 'index.html', 'home.html', 'index.php', 'portal.php']
request_line = compile("(\w+) (\S+) (HTTP/\d.\d)")


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
    _header = ''
    _body = ''

    def __init__(self, request):
        self.request = request
        self.status = request.request
        if self.status['Method'] == "OPTIONS": print "OPTIONS"
        if self.status['Method'] == "GET":
            status_code = check_file(self.status['Request-URI'])
            if status_code == 404:
                self.header_404()
            elif status_code == 200:
                self.generate(self.status['Request-URI'])
            else:
                self.header_500()
        if self.status['Method'] == "HEAD": print "HEAD"
        if self.status['Method'] == "POST": print "POST"
        if self.status['Method'] == "PUT": print "PUT"
        if self.status['Method'] == "DELETE": print "DELETE"
        if self.status['Method'] == "TRACE": print "TRACE"
        if self.status['Method'] == "CONNECT": print "CONNECT"

    def header_404(self):
        self._header += StatusLine(self.status['HTTP-Version'], 404).line + \
                        General().generate() + \
                        "Location: {}".format(self.status['Request-URI']) + \
                        "Retry-After: {}".format(120)

    def header_500(self):
        self._header += StatusLine(self.status['HTTP-Version'],
                                   500).line + General().generate() + HResponse().generate()

    # "Age: {}".format(int(round((time() - self._start) * 1000))) + CRLF + \
    def generate(self, body_file=None):
        if body_file is None:
            return self._header + self._body
        else:
            with safe_open(self.status['Request-URI']) as content_file:
                content = content_file.read()
            p = StatusLine(self.status['HTTP-Version'], 200).line + \
                General(trans_encode="gzip").generate() + \
                Entity(ctype="text/html", cl=self.request.enforces['language'][0], clen=content.__len__()).generate() + \
                content
            return p


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

    def __init__(self, data):
        self.func_dict = {
            'Accept:': self.accept,
            'Accept-Charset:': self.accept_charset,
            'Accept-Encoding:': self.accept_encoding,
            'Accept-Language:': self.accept_language,
            'Authorization:': self.authorization,
            'Expect:': self.expect,
            'From:': self._from,
            'Host:': self.host,
            'If-Match:': self.if_match,
            'If-Modified-Since:': self.if_modified_since,
            'If-None-Match:': self.if_none_match,
            'If-Range': self.if_range,
            'If-Unmodified-Since:': self.if_modified_since,
            'Max-Forwards:': self.max_forwards,
            'Proxy-Authorization:': self.proxy_authorization,
            'Range:': self.range,
            'Referer:': self.referer,
            'TE:': self.te,
            'User-Agent:': self.user_agent
        }

        self.lines = data.splitlines()
        self.message = request_line.match(self.lines[0]).groups(0)
        self.request = {  # Request Line
            'Method': self.message[0],
            'Request-URI': self.message[1],
            'HTTP-Version': self.message[2]
        }
        for line in self.lines:
            # If it exists, use it, if we're being fooled, don't.
            if self.func_dict.__contains__(line.split(" ")[0]):
                self.func_dict[line.split(" ")[0]](line)

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


def handle(data):
    request = Request(data)
    return Response(request)
