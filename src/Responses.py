import FileManager
import Header
from Config import CRLF, ALLOW, ALLOW_ADMIN  # DocumentRoot Constant
from Status import STATUS_CODE

SP = " "  # For more readability sake


def can(is_admin, perm):
    if is_admin: return True
    if ALLOW.__contains__(perm): return True
    return False


class Response:
    fetched = None
    status_code = 500  # Default to internal server error.

    def __init__(self, request):
        self.client = request.client
        self.major_ver = request.request['HTTP-Version'][0]
        self.minor_ver = request.request['HTTP-Version'][1]
        self.response_ver = "HTTP/{}.{}".format(self.major_ver, self.minor_ver)
        self.path = request.request['Request-URI']
        self.method = request.request['Method']
        self.general_header = Header.General()
        self.response_header = Header.Response()
        self.entity_header = Header.Entity()

    def dispatch(self, message_body=None):
        reqline = self.response_ver + SP + str(self.status_code) + SP + STATUS_CODE[self.status_code] + CRLF
        self.general_header.update()
        self.response_header.update()
        self.entity_header.update()
        if message_body is None:
            message_body = ""  # Gets rid of errors, also makes code easier to read.
        print "Responding:", reqline
        return reqline + self.general_header.header + self.response_header.header + \
               self.entity_header.header + CRLF + message_body

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        return self

    def generate(self):
        return self.dispatch()


class Get(Response):
    def __init__(self, request):
        Response.__init__(self, request)
        self.fetched = FileManager.FetchedFile(self.path)
        self.status_code = self.fetched.status_code
        self.message_body = ""

        if not FileManager.allowed_access(self.client, self.fetched.path):
            self.status_code = 403

        if self.status_code == 404:
            self.response_header.etag = self.fetched.checksum
            self.response_header.retry = 120
            self.entity_header.c_length = 0
        elif self.status_code == 200:
            self.general_header.cach = "max-age=120"
            self.entity_header.c_type = self.fetched.type
            self.entity_header.c_length = self.fetched.size
            self.entity_header.c_encoding = "gzip"
            self.response_header.retry = 120
            self.message_body += self.fetched.encoded
            self.message_body += CRLF
        elif self.status_code == 403:
            self.entity_header.c_len = 0

    def generate(self):
        return self.dispatch(self.message_body)


class Options(Response):
    def __init__(self, request):
        Response.__init__(self, request)
        self.status_code = 200
        self.entity_header.allow = ", ".join(ALLOW)
        if self.client.admin:
            self.entity_header.allow += ", ".join(ALLOW_ADMIN)


def error_response(request, status_code=500):
    return Response(request).__setattr__('status_code', status_code)


def not_implemented(request):
    return error_response(request, 501)
