from time import time, strftime, gmtime

from Config import LF


# cach = Cache-Control # conn = Connection
# prag = Pragma        # trai = Trailer
# t_en = Transfer-Enc..# upgr = Upgrade
# via  = Via           # warn = Warning
class General:
    def __init__(self, cach=None, conn=None, prag=None, trai=None, t_en=None,
                 upgr=None, via=None, warn=None):
        self.header = ""
        self.cach = cach
        self.conn = conn
        self.prag = prag
        self.trai = trai
        self.t_en = t_en
        self.upgr = upgr
        self.via = via
        self.warn = warn
        self.date = None
        self.update()

    def update(self):
        self.header = ""
        self.date = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())
        if self.cach is not None: self.header += "Cache-Control: {}".format(self.cach) + LF
        if self.conn is not None: self.header += "Connection: {}".format(self.conn) + LF
        if self.prag is not None: self.header += "Pragma: {}".format(self.prag) + LF
        if self.trai is not None: self.header += "Trailer: {}".format(self.trai) + LF
        if self.t_en is not None: self.header += "Transfer-Encoding: {}".format(self.t_en) + LF
        if self.upgr is not None: self.header += "Upgrade: {}".format(self.upgr) + LF
        if self.via is not None: self.header += "Via: {}".format(self.via) + LF
        if self.warn is not None: self.header += "Warning: {}".format(self.warn) + LF
        self.header += "Date: {}".format(self.date) + LF

    def setvar(self, var, val):
        setattr(self, var, val)


class Entity:
    def __init__(self, allow=None, c_enc=None, clang=None, c_len=None, c_loc=None, c_md5=None,
                 _rang=None, ctype=None, vary=None, exp=None, mod=None):
        self.header = None
        self.allow = allow
        self.c_encoding = c_enc
        self.c_language = clang
        self.c_length = c_len
        self.c_location = c_loc
        self.c_md5 = c_md5
        self.c_range = _rang
        self.c_type = ctype
        self.vary = vary
        self.expires = exp
        self.last_modified = mod
        self.update()

    def update(self):
        self.header = ""
        if self.allow is not None:          self.header += "Allow: {}".format(self.allow) + LF
        if self.c_encoding is not None:     self.header += "Content-Encoding: {}".format(self.c_encoding) + LF
        if self.c_language is not None:     self.header += "Content-Language: {}".format(self.c_language) + LF
        if self.c_length is not None:       self.header += "Content-Length: {}".format(self.c_length) + LF
        if self.c_location is not None:     self.header += "Content-Location: {}".format(self.c_location) + LF
        if self.c_md5 is not None:          self.header += "Content-MD5: {}".format(self.c_md5) + LF
        if self.c_range is not None:        self.header += "Content-Range: {}".format(self.c_range) + LF
        if self.c_type is not None:         self.header += "Content-Type: {}".format(self.c_type) + LF
        if self.vary is not None:           self.header += "Vary: Accept-Encoding" + LF
        if self.expires is not None:        self.header += "Expires: {}".format(self.expires) + LF
        if self.last_modified is not None:  self.header += "Last-Modified: {}".format(self.last_modified) + LF

    def setvar(self, var, val):
        setattr(self, var, val)


class Response:
    def __init__(self, ranges=None, age=None, etag=None, location=None, proxy_authenticate=None,
                 retry=None, vary=None, www_authenticate=None):
        self.header = ""
        self.ranges = ranges
        self.start_time = time() if age else None
        self.age = age
        self.etag = "\"" + etag + "\"" if etag is not None else None
        self.location = location
        self.p_authenticate = proxy_authenticate
        self.retry = retry
        self.server = 'PyWeb'
        self.vary = vary
        self.www_authenticate = www_authenticate

    def update(self):
        self.header = ""
        if self.ranges is not None:           self.header += "Accept-Ranges: {}".format(self.ranges) + LF
        if self.age is not None:              self.header += "Age: {}".format(int(round(time() - self.start_time))) + LF
        if self.etag is not None:             self.header += "E-Tag: {}".format(self.etag) + LF
        if self.location is not None:         self.header += "Location: {}".format(self.location) + LF
        if self.p_authenticate is not None:   self.header += "Proxy-Authenticate: {}".format(self.p_authenticate) + LF
        if self.retry is not None:            self.header += "Retry: {}".format(self.retry) + LF
        if self.server is not None:           self.header += "Server: {}".format(self.server) + LF
        if self.vary is not None:             self.header += "Vary: {}".format(self.vary) + LF
        if self.www_authenticate is not None: self.header += "WWW-Authenticate: {}".format(self.www_authenticate) + LF

    def setvar(self, var, val):
        setattr(self, var, val)
