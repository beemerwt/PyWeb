import gzip
import shutil
from glob import glob
from os import remove, path
from os.path import isfile

from Config import DOCUMENT_ROOT
from Definitions import CHECKSUMS

types = ("*.html", "*.htm", "*.php")


# path  - The path to be made absolute
# rpath - The path including DocumentRoot


def compress(rpath):
    with open(rpath, 'rb') as f_in, gzip.open(rpath + '.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def decompress(rpath):
    with gzip.open(rpath, 'rb') as f:
        file_content = f.read()
        print file_content


def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()


# "Grabs" the Checksum of file.
# This is the E-Tag
def grab(rpath):
    return CHECKSUMS[rpath] if CHECKSUMS.__contains__(rpath) else None


def cache_all():
    print "Caching all resources in", DOCUMENT_ROOT
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob(DOCUMENT_ROOT + files))
    for _file in files_grabbed:
        if not path.isfile(_file + '.gz'):  # If we already have it cached, don't re-cache. Use clear_cache to force
            compress(_file)


def clear_cache():
    files_grabbed = glob(DOCUMENT_ROOT + "*.gz")
    for _file in files_grabbed:
        remove(_file)


# Call path WITHOUT DocumentRoot
def is_cached(path):
    return isfile(path + ".gz")
