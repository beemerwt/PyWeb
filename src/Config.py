from ConfigParser import ConfigParser


class MasterConfig(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)
        ConfigParser.read(self, '../resources/Config.ini')


Config = MasterConfig()
DOCUMENT_ROOT = Config.get("DocumentRoot", "root")
