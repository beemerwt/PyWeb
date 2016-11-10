from ConfigParser import ConfigParser


class MasterConfig(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)
        ConfigParser.read(self, '../resources/Config.ini')


Config = MasterConfig()
DOCUMENT_ROOT = Config.get("DocumentRoot", "root")
CACHE_ROOT = Config.get("CacheRoot", "root")
CRLF = str(Config.get("NewLine", "CRLF", raw=True).replace("\\r", "\r").replace("\\n", "\n"))
LF = str(Config.get("NewLine", "LF", raw=True).replace("\\r", "\r").replace("\\n", "\n"))
