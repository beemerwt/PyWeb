import sys
from glob import glob
from os.path import basename

from Config import LOG_PLUGINS
from Delegate import Delegate

sys.path.append("../plugins/")


# obj is the module as a string.
# funcorclass is the function or class inside module as string.
def create_delegate(obj, funcorclass):
    if hasattr(sys.modules[obj], funcorclass):
        if sys.modules[obj].__name__ != Delegate.__name__:
            setattr(sys.modules[obj], funcorclass, Delegate(
                getattr(sys.modules[obj], funcorclass)))
        return getattr(sys.modules[obj], funcorclass)


def get_plugins():
    list_imports = glob("../plugins/*.py")
    for item in list_imports:
        plugin = basename(item).split(".")[0]
        __import__(plugin)
        if LOG_PLUGINS:
            print "Plugin \"" + plugin + "\" loaded."
