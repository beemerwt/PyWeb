import re
import sys
from StringIO import StringIO
from contextlib import contextmanager
from gzip import GzipFile

import FileManager
from Plugins import create_delegate

Fetcher = create_delegate("FileManager", "FetchedFile")


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


@Fetcher.callback
class Parser:
    command_line = re.compile("(    |\t){1}", flags=re.U)
    globals = {}
    locals = {}

    def __init__(self, fetchobj):
        check_ext = FileManager.get_extension(fetchobj.path)
        self.parent = fetchobj
        if check_ext != ".htm" and check_ext != ".php" and check_ext != ".html": return
        self.served = self.parent.original
        start_instances = [m.start() for m in re.finditer('<~', self.served)]
        end_instances = [m.start() for m in re.finditer('~>', self.served)]

        # Removes all BOA script and replaces it with it's executed implementation.
        for i in range(len(start_instances)):
            try:
                remove = self.parent.original[start_instances[i]:end_instances[i] + 2]
            except IndexError:
                remove = self.parent.original[start_instances[i]:]
            if remove is not None:
                self.served = self.served.replace(remove, self.parse(remove))

        encoded = StringIO()
        with GzipFile(fileobj=encoded, mode="w") as f:
            f.write(self.served)
        self.parent.encoded = encoded.getvalue()
        self.parent.size = len(encoded.getvalue())

    def __getattr__(self, item):
        return getattr(self.parent, item)

    # Parses and executes all BOA script
    def parse(self, code):
        code = code.replace("<~", "").replace("~>", "").splitlines()
        code[0] = code[0].lstrip()
        for i in range(len(code)):
            code[i] = self.command_line.sub("", code[i], 1)
        code = "\n".join(code)
        with stdout_io() as s:
            try:
                exec (code, self.globals, self.locals)
            except Exception as e:
                return str(e)
        # TRY to reduce errors.
        try:
            return s.getvalue()
        except UnicodeError:
            return ""
