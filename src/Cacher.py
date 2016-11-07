from glob import glob
from io import open
from os import remove, path
from os.path import isfile

from Config import DOCUMENT_ROOT
from LZ77 import LZ77Compressor

types = ("*.html", "*.htm", "*.php")
lz = LZ77Compressor()
checksums = []


def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()


# "Grabs" the Checksum of file.
# This is the E-Tag
def grab(path):
    return checksums[path] if checksums.__contains__(path) else None


def cache_all():
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob(DOCUMENT_ROOT + files))
    for _file in files_grabbed:
        if not path.isfile(_file + '.cache'):  # If we already have it cached, don't re-cache. Use clear_cache to force
            lz.compress(_file, output_file_path=(_file + '.cache'))


def clear_cache():
    files_grabbed = glob(DOCUMENT_ROOT + "*.cache")
    for _file in files_grabbed:
        remove(_file)


def get_file(path):
    if isfile(path + ".cache"):
        return open(path + ".cache", "rb")
    return open(path, "rb")
