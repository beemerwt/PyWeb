# This class is responsible for handling Requests.
from re import compile, match

import Responses
from Config import LOG_REQUEST

request_line = compile("(\w+) (\S+) HTTP/(\d).(\d)")
header_line = compile("([\w-]+):")
SP = " "


def sort_by_q(data):
    ret = []  # Make it a list instead of "None"
    for dat in data:
        ret.append(dat.split(";"))
    # Sort the list by the q value - if not q value then assume priority (1.0)
    ret.sort(key=lambda x: float(x[1][2:] if 1 < len(x) else 1.0), reverse=True)
    ret = [item[0] for item in ret]  # keep just the charsets, not qs
    return ret


class Request:
    enforces = {
        'charset': None,
        'encoding': None,
        'language': None,
        'authorization': None,
        'match': None,
        'unmod_since': None,
        'max_forwards': None,
        'expect': None
    }

    accept_types = []

    _host = None

    def __init__(self, client, data):
        self.client = client
        self.lines = data.splitlines()

        if LOG_REQUEST:
            print "Request Received:", client.client_address

        self.message = request_line.match(self.lines[0]).groups(0)
        self.request = {  # Request Line
            'Method': self.message[0],
            'Request-URI': self.message[1],
            'HTTP-Version': [self.message[2], self.message[3]]
        }
        for line in self.lines:
            # If it exists, use it, if we're being fooled, don't.
            if self.lines[0] == line:  # Skip the first line
                continue
            func = header_line.match(line)
            if func is not None:
                func = func.groups()[0].replace("-", "_").lower()  # Convert message to func-readable
                if func == "from":
                    self._from(line)
                if self.__contains__(func):
                    self[func](line)

    # For all functions below, data is a string of the full line.

    # Since this is a multi-threaded server, we do not need to implement "Accept" preferences.
    # All files get served as quickly as possible as soon as the message is received.
    def accept(self, data):
        pass

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
        pass

    def cache_control(self, data):
        pass

    def connection(self, data):
        pass

    def expect(self, data):
        data = match("(?=) (\S+)", data).groups(0)
        if data:
            self.enforces['expect'] = data

    # We will not be using FROM because it is simply too insecure.
    # Provided that we receive a request with "From," it is usually from a bot connection.
    # In this case, we'll do nothing as to not prevent anything "bad" from happening.
    # If you would like to change this behavior, create a plugin delegate for "Request", "Request"
    def _from(self, data):
        pass

    def host(self, data):
        self._host = match("Host: (\S+)", data).groups(0)

    def if_match(self, data):
        pass

    def if_modified_since(self, data):
        pass

    def if_none_match(self, data):
        pass

    def if_range(self, data):
        pass

    def if_unmodified_since(self, data):
        pass

    def max_forwards(self, data):
        pass

    def proxy_authorization(self, data):
        pass

    def range(self, data):
        pass

    def referer(self, data):
        pass

    def te(self, data):
        pass

    def user_agent(self, data):
        pass

    def upgrade_insecure_requests(self, data):
        pass

    def __getitem__(self, name):
        return getattr(self, name)

    def __contains__(self, item):
        return getattr(self, item, False)

    def respond(self):
        if not hasattr(Responses, self.request['Method'].title()):
            return Responses.not_implemented(self)

        # According to the HTTP Guidelines: We MUST reply 400 if no Host was provided.
        if self._host is None:
            return Responses.error_response(self, 400)

        # Since we are a multi-threaded server, we do not implement typical HTTP guidelines
        # Instead, we are implementing a kind of T/TCP which does not support 100-Continue
        # Good thing, 100-Continue doesn't really exist anymore.
        if self.enforces['expect']:
            return Responses.error_response(self, 417)

        return getattr(Responses, self.request['Method'].title())(self)
