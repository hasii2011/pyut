
from typing import List

from logging import Logger
from logging import getLogger

from glob import glob

from os import chdir
from os import getcwd
from os import path as osPath
from os import sep as osSep

from sys import path as sysPath

from org.pyut.errorcontroller.ErrorManager import ErrorManager
from org.pyut.general.Singleton import Singleton


class PluginManager(Singleton):

    PLUGIN_DIRECTORY = "plugins"

    """
    Interface between the application and the plugins.

    This class is responsible for searching for available plugins, loading them,
    extracting runtime information and providng the information to components that need it
    (for example the `AppFrame` to create the import/export submenus).

    @author Laurent Burgbacher <lb@alawa.ch>
    @version $Revision: 1.4 $

    @modified C.Dutoit <dutoitc@hotmail.com> oct02, added ToPlugins
    """
    def init(self):
        """
        Singleton Constructor.
        At init time, this class searches the PLUGIN_DIRECTORY.

        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        self.logger: Logger = getLogger(__name__)

        # Init
        self.ioPlugs: List[type] = []
        self.toPlugs: List[type] = []

        # get the file names
        saveDir = getcwd()
        self.logger.info(f'Save Directory: {saveDir}')
        PluginManager.findPluginDirectory()
        chdir(PluginManager.PLUGIN_DIRECTORY)
        sysPath.append(getcwd())
        ioPlugs: List[str] = glob("Io*.py")
        toPlugs: List[str] = glob("To*.py")
        chdir(saveDir)

        # remove extensions
        ioPlugsNoExt: List[str] = list(map(lambda x: osPath.splitext(x)[0], ioPlugs))
        toPlugsNoExt: List[str] = list(map(lambda x: osPath.splitext(x)[0], toPlugs))

        # Import plugins
        self.ioPlugs = self._loadPlugins(plugInNames=ioPlugsNoExt, pluginType='I/O')
        self.toPlugs = self._loadPlugins(plugInNames=toPlugsNoExt, pluginType='tool')

    def getPluginsInfo(self) -> List[str]:
        """
        Get textual information about available plugins.

        @return String []
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        s: List[str] = []
        for plug in self.ioPlugs + self.toPlugs:
            obj = plug(None, None)
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

    def _loadPlugins(self, plugInNames, pluginType: str) -> List[type]:
        """
        Load the plugin that are named
        Args:
            plugInNames: The list of plugin names
            pluginType:   Are they I/O plugins or tool plugins

        Returns:  A list of loaded modules
        """
        retLoadedPlugins: List[type] = []
        for plug in plugInNames:
            self.logger.info(f"Importing {pluginType} plugin from file {plug}")
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
                retLoadedPlugins.append(cl)
        return retLoadedPlugins

    @classmethod
    def findPluginDirectory(cls):
        """"""
        path = getcwd()
        if osPath.isdir(f'{path}{osSep}{PluginManager.PLUGIN_DIRECTORY}'):
            return
        else:
            chdir("../")
            cls.findPluginDirectory()
