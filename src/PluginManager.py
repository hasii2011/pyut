
from glob import glob

from os import chdir
from os import pardir
from os import getcwd
from os import path as osPath

from sys import exc_info
from sys import path as sysPath
from traceback import extract_tb

from logging import Logger
from logging import getLogger

# needed by the plugins
# from PyutClass      import PyutClass
# from PyutParam      import PyutParam
# from PyutMethod     import PyutMethod
# from PyutField      import PyutField
# from PyutStereotype import PyutStereotype
# from UmlFrame       import *
# from OglClass       import OglClass
# from OglLink        import *

from singleton import Singleton


class PluginManager(Singleton):
    """
    Interface between the application and the plugins.

    This class is responsible to search for available plugins, load them,
    extract runtime information and give the information to those who need it
    (for example the `AppFrame` to create the import/export submenus).

    @author Laurent Burgbacher <lb@alawa.ch>
    @version $Revision: 1.4 $

    @modified C.Dutoit <dutoitc@hotmail.com> oct02, added ToPlugins
    """
    def init(self):
        """
        Singleton Constructor.
        At init time, this class searches for the plugins in the plugins
        directory.

        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        self.logger: Logger = getLogger(__name__)

        # Init
        self.ioPlugs = []
        self.toPlugs = []

        # get the file names
        chdir("plugins")
        sysPath.append(getcwd())
        ioPlugs = glob("Io*.py")
        toPlugs = glob("To*.py")
        chdir(pardir)

        # remove extension
        ioPlugs = map(lambda x: osPath.splitext(x)[0], ioPlugs)
        toPlugs = map(lambda x: osPath.splitext(x)[0], toPlugs)

        # Import I/O plugins
        for plug in ioPlugs:
            self.logger.info(f"Importing I/O plugin from file {plug}")
            module = None
            try:
                module = __import__(plug)
            except (ValueError, Exception) as e:
                self.logger.error(f"Error importing plugin {plug} with message: {e}")
                self.logger.error(f"Error : {exc_info()[0]}")
                self.logger.error(f"Msg   : {exc_info()[1]}")
                self.logger.error(f"Trace :")
                for el in extract_tb(exc_info()[2]):
                    self.logger.error(el)
            if module is not None:
                # cl = eval("module.%s" % (module.__name__))
                pluginName: str = f"module.{module.__name__}"
                self.logger.info(f'Loading {pluginName}')
                cl = eval(pluginName)
                self.ioPlugs.append(cl)

        # Import tools plugins
        for plug in toPlugs:
            self.logger.info(f"Importing tool plugin from file {plug}")
            module = None
            try:
                module = __import__(plug)
            except (ValueError, Exception) as e:
                self.logger.error(f"Error importing plugin {plug} with message: {e}")
                self.logger.error(f"Error : {exc_info()[0]}")
                self.logger.error(f"Msg   : {exc_info()[1]}")
                self.logger.error(f"Trace :")
                for el in extract_tb(exc_info()[2]):
                    self.logger.error(el)
            if module is not None:
                cl = eval(f"module.{module.__name}")
                self.toPlugs.append(cl)

    def getPluginsInfo(self):
        """
        Get textual information about available plugins.

        @return String []
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        s = []
        for plug in self.ioPlugs + self.toPlugs:
            obj = plug(None, None)
            # s.append("Plugin : %s version %s (c) by %s" % (obj.getName(), obj.getVersion(), obj.getAuthor()))
            s.append(f"Plugin : {obj.getName()} version {obj.getVersion()} (c) by {obj.getAuthor()}")
        return s

    def getInputPlugins(self):
        """
        Get the input plugins.
        Returns a list of classes (the plugins classes).

        @return Class []
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        pluginList = []
        for plug in self.ioPlugs:
            obj = plug(None, None)
            if obj.getInputFormat() is not None:
                pluginList.append(plug)
        return pluginList

    def getOutputPlugins(self):
        """
        Get the output plugins.
        Returns a list of classes (the plugins classes).

        @return Class []
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        pluginList = []
        for plug in self.ioPlugs:
            obj = plug(None, None)
            if obj.getOutputFormat() is not None:
                pluginList.append(plug)
        return pluginList

    def getToolPlugins(self):
        """
        Get the tool plugins.
        Returns a list of classes (the plugins classes).

        @return Class []
        @author C.Dutoit <dutoitc@hotmail.com>
        @since 1.5.2.6
        """
        return self.toPlugs
#
#  TODO Put in Unit test
#
# def test():
#     p = PluginManager()
#     for info in p.getPluginsInfo():
#         print(info)
#
# if __name__ == "__main__": test()
#
