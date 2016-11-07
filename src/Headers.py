from hashlib import md5
from time import time, strftime, gmtime

from Config import LF


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
        if self.cache_control:      header += "Cache-Control: {}".format(self.cache_control) + LF
        if self.connection:         header += "Connection: {}".format(self.connection) + LF
        if self.date:               header += "Date: {}".format(self.date) + LF
        if self.pragma:             header += "Pragma: {}".format(self.pragma) + LF
        if self.trailer:            header += "Trailer: {}".format(self.trailer) + LF
        if self.transfer_encoding:  header += "Transfer-Encoding: {}".format(self.transfer_encoding) + LF
        if self.upgrade:            header += "Upgrade: {}".format(self.upgrade) + LF
        if self.via:                header += "Via: {}".format(self.via) + LF
        if self.warning:            header += "Warning: {}".format(self.warning) + LF
        return header


class Entity:
    def __init__(self, a=None, ce=None, cl=None, clen=None, cloc=None, cmd5=None,
                 crange=None, ctype=None, vary=None, exp=None, mod=None):
        self.allow = a
        self.c_encoding = ce
        self.c_language = cl
        self.c_length = clen
        self.c_location = cloc
        self.c_md5 = cmd5
        self.c_range = crange
        self.c_type = ctype
        self.vary = vary
        self.expires = exp
        self.last_modified = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()) if mod else None

    def generate(self):
        header = ""
        if self.allow is not None:          header += "Allow: {}".format(self.allow) + LF
        if self.c_encoding is not None:     header += "Content-Encoding: {}".format(self.c_encoding) + LF
        if self.c_language is not None:     header += "Content-Language: {}".format(self.c_language) + LF
        if self.c_length is not None:       header += "Content-Length: {}".format(self.c_length) + LF
        if self.c_location is not None:     header += "Content-Location: {}".format(self.c_location) + LF
        if self.c_md5 is not None:          header += "Content-MD5: {}".format(self.c_md5) + LF
        if self.c_range is not None:        header += "Content-Range: {}".format(self.c_range) + LF
        if self.c_type is not None:         header += "Content-Type: {}".format(self.c_type) + LF
        if self.vary is not None:           header += "Vary: Accept-Encoding" + LF
        if self.expires is not None:        header += "Expires: {}".format(self.expires) + LF
        if self.last_modified is not None:  header += "Last-Modified: {}".format(self.last_modified) + LF
        return header


class Response:
    def __init__(self, ranges=None, age=None, etag=None, location=None, proxy_authenticate=None,
                 retry=None, vary=None, www_authenticate=None):
        self.ranges = ranges
        self.start_time = time() if age else None
        self.age = age
        self.etag = "\"" + md5(etag).hexdigest() + "\"" if etag is not None else None
        self.location = location
        self.proxy_authenticate = proxy_authenticate
        self.retry = retry
        self.server = 'PyWeb'
        self.vary = vary
        self.www_authenticate = www_authenticate

    def generate(self):
        header = ""
        if self.ranges:             header += "Accept-Ranges: {}".format(self.ranges) + LF
        if self.age:                header += "Age: {}".format(int(round(time() - self.start_time))) + LF
        if self.etag:               header += "E-Tag: {}".format(self.etag) + LF
        if self.location:           header += "Location: {}".format(self.location) + LF
        if self.proxy_authenticate: header += "Proxy-Authenticate: {}".format(self.proxy_authenticate) + LF
        if self.retry:              header += "Retry: {}".format(self.retry) + LF
        if self.server:             header += "Server: {}".format(self.server) + LF
        if self.vary:               header += "Vary: {}".format(self.vary) + LF
        if self.www_authenticate:   header += "WWW-Authenticate: {}".format(self.www_authenticate) + LF
        return header
