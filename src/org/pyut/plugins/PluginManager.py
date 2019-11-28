
from logging import Logger
from logging import getLogger

from glob import glob

from os import chdir
from os import getcwd
from os import path as osPath
from os import sep as osSep

from sys import exc_info
from sys import path as sysPath
from traceback import extract_tb

from org.pyut.errorcontroller.ErrorManager import ErrorManager
from org.pyut.general.Singleton import Singleton


class PluginManager(Singleton):

    PLUGIN_DIRECTORY = "plugins"

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
        At init time, this class searches for the %s in the plugins
        directory.

        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        self.logger: Logger = getLogger(__name__)

        # Init
        self.ioPlugs = []
        self.toPlugs = []

        # get the file names
        saveDir = getcwd()
        self.logger.info(f'Save Directory: {saveDir}')
        PluginManager.findPluginDirectory()
        chdir(PluginManager.PLUGIN_DIRECTORY)
        # chdir('fake')
        sysPath.append(getcwd())
        ioPlugs = glob("Io*.py")
        toPlugs = glob("To*.py")
        chdir(saveDir)

        # remove extension
        ioPlugs = map(lambda x: osPath.splitext(x)[0], ioPlugs)
        toPlugs = map(lambda x: osPath.splitext(x)[0], toPlugs)
        #
        # TODO:  Remove this duplicated code by calling a common method
        #
        # Import I/O plugins
        for plug in ioPlugs:
            self.logger.info(f"Importing I/O plugin from file {plug}")
            module = None
            try:
                module = __import__(plug)
            except (ValueError, Exception) as e:
                self.logger.error(f"Error importing plugin {plug} with message: {e}")
                eMsg: str = ErrorManager.getErrorInfo()
                self.logger.error(eMsg)
            if module is not None:
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
                eMsg: str = ErrorManager.getErrorInfo()
                self.logger.error(eMsg)
            if module is not None:
                self.logger.info(f'plugin imported {plug}')
                cl = eval(f"module.{module.__name__}")
                self.logger.info(f'plugin eval`ed {plug}')
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

    @classmethod
    def findPluginDirectory(cls):
        """"""
        path = getcwd()
        if osPath.isdir(f'{path}{osSep}{PluginManager.PLUGIN_DIRECTORY}'):
            return
        else:
            chdir("../")
            cls.findPluginDirectory()

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
