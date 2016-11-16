import re
import sys
from StringIO import StringIO
from contextlib import contextmanager
from gzip import GzipFile

import FileManager
from Config import CRLF
from Plugins import create_delegate

Get_Response = create_delegate("Responses", "Get")
command_line = re.compile("(    |\t){1}", flags=re.U)

# When getting the "served" part of a file, get rid of the BOAscript
# Assign Parser.read() to read bytes, as the FileManager does normally


@contextmanager
def stdout_io(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@Get_Response.callback
def parser(returned_get):
    if returned_get.status_code != 200: return None  # If and only if we're serving the file.
    check_ext = FileManager.get_extension(returned_get.fetched.path)
    if check_ext != ".htm" and check_ext != ".php" and check_ext != ".html": return None

    global_ = {}
    local_ = {}

    served = returned_get.fetched.original
    start_instances = [m.start() for m in re.finditer('<~', served)]
    end_instances = [m.start() for m in re.finditer('~>', served)]

    # Removes all BOA script and replaces it with it's executed implementation.
    for i in range(len(start_instances)):
        try:
            remove = returned_get.fetched.original[start_instances[i]:end_instances[i] + 2]
        except IndexError:
            remove = returned_get.fetched.original[start_instances[i]:]
        if remove is not None:
            served = served.replace(remove, parse(remove, global_, local_))

    encoded = StringIO()
    with GzipFile(fileobj=encoded, mode="w") as f:
        f.write(served)
    returned_get.message_body = encoded.getvalue() + CRLF
    returned_get.entity_header.c_length = len(encoded.getvalue())
    return returned_get


# Parses and executes all BOA script
def parse(code, *scope):
    code = code.replace("<~", "").replace("~>", "").splitlines()
    code[0] = code[0].lstrip()
    for i in range(len(code)):
        code[i] = command_line.sub("", code[i], 1)
    code = "\n".join(code)
    with stdout_io() as s:
        try:
            exec code in scope[0], scope[1]
        except Exception as e:
            return str(e)
    # TRY to reduce errors.
    try:
        return s.getvalue()
    except UnicodeError:
        return ""
