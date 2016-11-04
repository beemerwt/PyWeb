from time import strftime, gmtime
from Parser import safe_open

response = "HTTP/1.1 {}"
date = "Date: {}"
server = "Server: PyWeb"
last_modified = "Last-Modified: {}"
accept_ranges = "Accept-Ranges: {}"
content_length = "Content-Length: {}"
vary = "Vary: {}"
content_type = "Content-Type: {}"
content = "{}"

# Response  = Status-Line
#               *(( general-header
#                | response-header
#                | entity-header ) CRLF)
#               CRLF
#               [ message-body ]


class Request:
    def __init__(self, data):
        self.message = data.splitlines()
        self.info = self.message[0].split(" ")
        self.type = self.info[0]
        self.path = self.info[1]
        self.ver = self.info[2]
        self.file = safe_open(self.path)
        self.date = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())
        self.last_modified = None
        self.accept_ranges = None
        self.content_length = None
        self.vary = None
        self.content_type = None
        self.content = None

        # Check for status codes...
        if self.file == 404:
            self.response = "404 Not Found"
        else:  # Otherwise, just send a default message with the content.
            self.last_modified = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())  # getmtime(self.path)
            self.accept_ranges = "bytes"
            self.content_length = 26  # getsize(self.path)
            self.vary = "Accept-Encoding"
            self.content_type = "text/html"  # Default HTML.
            self.response = "200 OK"  # Default to successful response
            self.content = "<html><h1>Test</h1></html>"  # Default nothing.

    def create_response(self):
        local_return = ""
        local_return += response.format(self.response)
        local_return += date.format(self.date)
        if self.last_modified:
            local_return += last_modified.format(self.last_modified)
        if self.accept_ranges:
            local_return += accept_ranges.format(self.accept_ranges)
        if self.content_length:
            local_return += content_length.format(self.content_length)
        if self.vary:
            local_return += vary.format(self.vary)
        if self.content_type:
            local_return += content_type.format(self.content_type)
        if self.content:
            local_return += content.format(self.content)

        return local_return


def handle(data):
    request = Request(data)
    return request.create_response()
