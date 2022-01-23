
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from os import sep as osSep

from wx import NewIdRef

from org.pyut.general.Singleton import Singleton

from org.pyut.plugins.io.IoCpp import IoCpp
from org.pyut.plugins.io.IoDTD import IoDTD
from org.pyut.plugins.io.IoGML import IoGML
from org.pyut.plugins.io.IoImage import IoImage
from org.pyut.plugins.io.IoJava import IoJava
from org.pyut.plugins.io.IoJavaReverse import IoJavaReverse
from org.pyut.plugins.io.IoJavascript import IoJavascript
from org.pyut.plugins.io.IoPdf import IoPdf
from org.pyut.plugins.io.IoPython import IoPython
from org.pyut.plugins.io.IoWxImage import IoWxImage
from org.pyut.plugins.io.IoXmi import IoXmi
from org.pyut.plugins.io.IoXmiOMG import IoXmi_OMG
from org.pyut.plugins.io.IoXml import IoXml
from org.pyut.plugins.io.IoXSD import IoXSD

from org.pyut.plugins.tools.ToArrangeLinks import ToArrangeLinks
from org.pyut.plugins.tools.ToAscii import ToAscii
from org.pyut.plugins.tools.ToCDAutoLayout import ToCDAutoLayout
from org.pyut.plugins.tools.ToFastEdit import ToFastEdit
from org.pyut.plugins.tools.ToLayout import ToLayout
from org.pyut.plugins.tools.ToLayoutSave import ToLayoutSave
from org.pyut.plugins.tools.ToOrthogonalLayoutV2 import ToOrthogonalLayoutV2
from org.pyut.plugins.tools.ToSugiyama import ToSugiyama
from org.pyut.plugins.tools.ToTransforms import ToTransforms
from org.pyut.ui.tools.SharedTypes import PluginList
from org.pyut.ui.tools.SharedTypes import PluginMap

FileNameListType = List[str]


class PluginManager(Singleton):

    PLUGIN_DIRECTORY: str = f"org{osSep}pyut{osSep}plugins"
    PLUGIN_PACKAGE:   str = 'org.pyut.plugins'

    IO_PLUGINS: PluginList = PluginList([IoCpp, IoDTD, IoJava, IoJavaReverse,
                                         IoJavascript, IoPython, IoXmi, IoXmi_OMG,
                                         IoXml, IoXSD, IoGML, IoPdf, IoImage, IoWxImage,
                                         ])
    TOOL_PLUGINS: PluginList = PluginList([ToArrangeLinks, ToAscii, ToCDAutoLayout,
                                           ToFastEdit, ToLayout, ToLayoutSave,
                                           ToOrthogonalLayoutV2, ToSugiyama, ToTransforms
                                           ])

    """
    Interface between the application and the plugins.

    Identifies all the known plugins
    """
    def init(self):
        """
        Singleton Constructor.
        """
        self.logger: Logger = getLogger(__name__)

    def getPluginsInfo(self) -> List[str]:
        """
        Get textual information about available plugins.

        Returns:  A string list
        """
        s: List[str] = []
        for plug in self.IO_PLUGINS + self.TOOL_PLUGINS:
            obj = plug(None, None)
            s.append(f"Plugin : {obj.getName()} version {obj.getVersion()} (c) by {obj.getAuthor()}")
        return s

    def getInputPlugins(self) -> PluginList:
        """
        Get the input plugins.

        Returns:  A list of classes (the plugins classes).
        """

        pluginList = cast(PluginList, [])
        for plug in self.IO_PLUGINS:
            obj = plug(None, None)
            if obj.getInputFormat() is not None:
                pluginList.append(plug)
        return pluginList

    def getOutputPlugins(self) -> PluginList:
        """
        Get the output plugins.

        Returns:  A list of classes (the plugins classes).
        """
        pluginList = cast(PluginList, [])
        for plug in self.IO_PLUGINS:
            obj = plug(None, None)
            if obj.getOutputFormat() is not None:
                pluginList.append(plug)
        return pluginList

    def getToolPlugins(self) -> PluginList:
        """
        Get the tool plugins.

        Returns:    A list of classes (the plugins classes).
        """
        return self.TOOL_PLUGINS

    def mapWxIdsToToolPlugins(self) -> PluginMap:

        plugins: PluginList = self.getToolPlugins()

        pluginMap: PluginMap = self.__mapWxIdsToPlugins(plugins)

        return pluginMap

    def mapWxIdsToImportPlugins(self) -> PluginMap:

        plugins: PluginList = self.getInputPlugins()

        pluginMap: PluginMap = self.__mapWxIdsToPlugins(plugins)

        return pluginMap

    def mapWxIdsToExportPlugins(self) -> PluginMap:

        plugins: PluginList = self.getOutputPlugins()

        pluginMap: PluginMap = self.__mapWxIdsToPlugins(plugins)

        return pluginMap

    def __mapWxIdsToPlugins(self, plugins: List[type]) -> PluginMap:

        pluginMap: PluginMap = cast(PluginMap, {})

        nb: int = len(plugins)

        for x in range(nb):
            wxId: int = NewIdRef()

            pluginMap[wxId] = plugins[x]

        return pluginMap
