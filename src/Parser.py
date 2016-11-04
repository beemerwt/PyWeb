import os, io
default_files = ['index.htm', 'index.html', 'home.html', 'index.php', 'portal.php']


def safe_open(path):
    if path == "/":
        for fname in default_files:
            if os.path.isfile(fname):
                return io.open(fname, "r")
    if os.path.isfile(path):
        return io.open(path, "r")
    return 404
