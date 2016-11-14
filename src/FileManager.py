from StringIO import StringIO
from gzip import GzipFile
from hashlib import md5
from io import open as _open
from os.path import getsize, isfile, relpath, splitext

from Config import DOCUMENT_ROOT
from Definitions import DEFAULT_FILES, CHECKSUMS


# FetchedFile class
# Path should be non-absolute
class FetchedFile:
    def __init__(self, path):
        self.path = get_absolute_path(path)
        self.status_code = check(self.path)
        self.checksum = get_checksum(self.path)
        self.original = open(self.path).read()  # Call "open" for delegate functionality.
        self.encoded = StringIO()
        with GzipFile(fileobj=self.encoded, mode="w") as f:
            f.write(self.original)
        self.encoded = self.encoded.getvalue()
        self.size = len(self.encoded)
        self.extension = get_extension(self.path)
        self.type = get_type(self.extension)


# Gets the safe version of the path.
# For example, if we're give "/", we need the DocumentRoot's INDEX file.
# INDEX files are determined in the config, order precedent
def get_safe(path):
    if path.endswith("/"): return next(
        DOCUMENT_ROOT + _file for _file in DEFAULT_FILES if isfile(DOCUMENT_ROOT + _file))
    if isfile(relpath(DOCUMENT_ROOT + path)): return path[1:]  # get rid of the slash in front of the path.
    return None


# gets the type of the extension (data)
def get_type(data):
    if data == ".html" or data == ".htm" or data == ".php": return "text/html"
    if data == ".png": return "image/png"
    if data == ".bmp": return "image/bmp"
    if data == ".gif": return "image/gif"
    if data == ".css" or data == ".xcss": return "text/css"
    if data == ".js": return "text/js"
    if data == ".jpeg" or data == ".jpg": return "image/jpeg"
    if data == ".json": return "application/json"
    if data == ".pdf": return "application/pdf"
    return "text/plain"


# Returns the filename of the given path
def get_absolute_file(path, ext=True):
    newpath = get_safe(path)
    if newpath is not None:
        filename, file_extension = splitext(path)
        filename = filename[filename.rfind("/"):]
        return filename + (file_extension if ext else "")


# Splits the file or path given, gives the extension.
# May not be accurate 100% of the time (.tar.gz returns ".gz")
def get_extension(path):
    filename, file_extension = splitext(path)
    return file_extension


# Returns the absolute path of the given file.
# Path is assumed DOCUMENT_ROOT+
def get_absolute_path(_file):
    newfile = get_safe(_file)
    return relpath(DOCUMENT_ROOT + newfile)


# Path is assumed absolute
def size(path):
    return getsize(path)


# Overrides io.open/__builtin__.open in order to normalize openings.
# Path is assumed absolute
def open(path):
    return _open(path, "rb")


# Status code check for the absolute path, if not exists returns "404" (Not Found)
def check(path):
    if not isfile(path): return 404
    return 200


# Gets the checksum of the path, assumed absolute
# Stores if not already found.
def get_checksum(path):
    if path is None: return
    if path in CHECKSUMS: return CHECKSUMS[path]
    c = md5(open(path).read()).hexdigest()
    CHECKSUMS[path] = c
    return CHECKSUMS[path]


'''
def compress(_file):
    print "Creating cache of file:", _file
    if not isdir(CACHE_ROOT + _file):
        mkpath(dirname(CACHE_ROOT + _file))
    with open(relpath(DOCUMENT_ROOT + _file), 'rb') as f_in, gzip.open(CACHE_ROOT + _file + '.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
'''
