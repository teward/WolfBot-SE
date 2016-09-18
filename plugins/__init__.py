from os.path import dirname, basename, isfile
import glob

def getPlugins():
    modules = glob.glob(dirname(__file__)+"/*.py")
    return [ basename(f)[:-3] for f in modules if isfile(f)]

__all__ = getPlugins()
