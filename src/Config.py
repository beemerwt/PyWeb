from ConfigParser import ConfigParser


class MasterConfig(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)
        ConfigParser.read(self, '../resources/Config.ini')


Config = MasterConfig()
DOCUMENT_ROOT = Config.get("DocumentRoot", "root")

CRLF = str(Config.get("NewLine", "CRLF", raw=True).replace("\\r", "\r").replace("\\n", "\n"))
LF = str(Config.get("NewLine", "LF", raw=True).replace("\\r", "\r").replace("\\n", "\n"))

ADMIN_LIST = Config.get("Admin", "ips")
ALLOW = Config.get("Allow", "HTTP")
ALLOW_ADMIN = Config.get("Allow", "ADMIN")

LOG_PLUGINS = Config.getboolean("Logging", "plugins")
LOG_ON_CONNECT = Config.getboolean("Logging", "on_connect")
LOG_ON_DISCONNECT = Config.getboolean("Logging", "on_disconnect")
LOG_REQUEST = Config.getboolean("Logging", "requests")
LOG_RESPONSE = Config.getboolean("Logging", "response")
LOG_RESPONSE_FULL = Config.getboolean("Logging", "response_fulltext")
