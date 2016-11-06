from re import compile
from time import time, strftime, gmtime

from Statuses import STATUS_CODE

CRLF = "\r\n"


class StatusLine:  # StatusLine.response is the line you want.
    re_ver = compile("HTTP/(\d).(\d)")
    line = "HTTP/{}.{} {} {}"

    def __init__(self, ver, code, opt=None):
        ver = self.re_ver.match(ver).groups(0)
        if not ver:
            ver = [1, 1]  # Default to 1.1 (Our server)
        if not opt:
            if not STATUS_CODE.__contains__(code):
                code = 500  # Default to 500 if we don't have the code. It's an error.
            self.line = self.line.format(ver[0], ver[1], code, STATUS_CODE[code]) + CRLF
        else:
            self.line = self.line.format(ver[0], ver[1], code, opt) + CRLF


class General:
    def __init__(self, cache=None, conn=None, pragma=None, trailer=None, trans_encode=None,
                 upgrade=None, via=None, warning=None):
        self.cache_control = cache
        self.connection = conn
        self.date = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())
        self.pragma = pragma
        self.trailer = trailer
        self.transfer_encoding = trans_encode
        self.upgrade = upgrade
        self.via = via
        self.warning = warning

    # Generate general header in order.
    def generate(self):
        header = ""
        if self.cache_control:      header += "Cache-Control: {}".format(self.cache_control)
        if self.connection:         header += "Connection: {}".format(self.connection)
        if self.date:               header += "Date: {}".format(self.date)
        if self.pragma:             header += "Pragma: {}".format(self.pragma)
        if self.trailer:            header += "Trailer: {}".format(self.trailer)
        if self.transfer_encoding:  header += "Transfer-Encoding: {}".format(self.transfer_encoding)
        if self.upgrade:            header += "Upgrade: {}".format(self.upgrade)
        if self.via:                header += "Via: {}".format(self.via)
        if self.warning:            header += "Warning: {}".format(self.warning)
        return header


class Entity:
    def __init__(self, a=None, ce=None, cl=None, clen=0, cloc=None, cmd5=None,
                 crange=None, ctype=None, exp=None, mod=None):
        self.allow = a
        self.c_encoding = ce
        self.c_language = cl
        self.c_length = clen
        self.c_location = cloc
        self.c_md5 = cmd5
        self.c_range = crange
        self.c_type = ctype
        self.expires = exp
        self.last_modified = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()) if mod else None

    def generate(self):
        header = ""
        if self.allow:          header += "Allow: {}".format(self.allow)
        if self.c_encoding:     header += "Content-Encoding: {}".format(self.c_encoding)
        if self.c_language:     header += "Content-Language: {}".format(self.c_language)
        if self.c_length:       header += "Content-Length: {}".format(self.c_length)
        header += "Vary: Accept-Encoding"
        if self.c_location:     header += "Content-Location: {}".format(self.c_location + 4)
        if self.c_md5:          header += "Content-MD5: {}".format(self.c_md5)
        if self.c_range:        header += "Content-Range: {}".format(self.c_range)
        if self.c_type:         header += "Content-Type: {}".format(self.c_type)
        if self.expires:        header += "Expires: {}".format(self.expires)
        if self.last_modified:  header += "Last-Modified: {}".format(self.last_modified)
        return header


class Builder:
    def __init__(self, *header):
        return

    def generate(self):
        return


class Response:
    def __init__(self, ranges=None, age=None, etag=None, location=None, proxy_authenticate=None,
                 retry=None, vary=None, www_authenticate=None):
        self.ranges = ranges
        self.start_time = time() if age else None
        self.age = age
        self.etag = etag
        self.location = location
        self.proxy_authenticate = proxy_authenticate
        self.retry = retry
        self.server = 'PyWeb'
        self.vary = vary
        self.www_authenticate = www_authenticate

    def generate(self):
        header = ""
        if self.ranges:             header += "Accept-Ranges: {}".format(self.ranges)
        if self.age:                header += "Age: {}".format(int(round(time() - self.start_time)))
        if self.etag:               header += "E-Tag: {}".format(self.etag)
        if self.location:           header += "Location: {}".format(self.location)
        if self.proxy_authenticate: header += "Proxy-Authenticate: {}".format(self.proxy_authenticate)
        if self.retry:              header += "Retry: {}".format(self.retry)
        if self.server:             header += "Server: {}".format(self.server)
        if self.vary:               header += "Vary: {}".format(self.vary)
        if self.www_authenticate:   header += "WWW-Authenticate: {}".format(self.www_authenticate)
        return header
