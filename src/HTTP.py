from time import strftime, gmtime

response = '''
HTTP/1.1 {} {}
Date: {}
Server: {}
Last-Modified: {}
Accept-Ranges: {}
Content-Length: {}
Vary: {}
Content-Type: {}

{}'''
SERVER = 'PyWeb'


class Request:
    def __init__(self, data):
        self.message = data.splitlines()
        self.info = self.message[0].split(" ")
        self.type = self.info[0]
        self.path = self.info[1]
        self.ver = self.info[2]

        self.date = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())
        self.last_modified = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())  # getmtime(self.path)
        self.accept_ranges = "bytes"
        self.content_length = 26  # getsize(self.path)
        self.vary = "Accept-Encoding"
        self.content_type = "text/html"  # Default HTML.
        self.response = "200"  # Default to successful response
        self.response_msg = "OK"  # Default to successful response message
        self.content = "<html><h1>Test</h1></html>"  # Default nothing.

    def create_response(self):
        return response.format(self.response, self.response_msg, self.date, SERVER, self.last_modified,
                               self.accept_ranges, self.content_length, self.vary, self.content_type, self.content)


def handle(data):
    request = Request(data)
    return request.create_response()
