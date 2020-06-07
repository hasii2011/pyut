
from typing import List

from logging import Logger
from logging import getLogger

from os import sep as osSep

from org.pyut.general.Singleton import Singleton

from org.pyut.plugins.io.IoCpp import IoCpp
from org.pyut.plugins.io.IoDTD import IoDTD
from org.pyut.plugins.io.IoGML import IoGML
from org.pyut.plugins.io.IoJava import IoJava
from org.pyut.plugins.io.IoJavaReverse import IoJavaReverse
from org.pyut.plugins.io.IoJavascript import IoJavascript
from org.pyut.plugins.io.IoPython import IoPython
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
from org.pyut.plugins.tools.ToPython import ToPython
from org.pyut.plugins.tools.ToSugiyama import ToSugiyama
from org.pyut.plugins.tools.ToTransforms import ToTransforms

FileNameListType = List[str]


class PluginManager(Singleton):

    PLUGIN_DIRECTORY: str = f"org{osSep}pyut{osSep}plugins"
    PLUGIN_PACKAGE:   str = 'org.pyut.plugins'

    IO_PLUGINS: List[type] = [IoCpp, IoDTD, IoJava, IoJavaReverse, IoJavascript,
                              IoPython, IoXmi, IoXmi_OMG, IoXml, IoXSD, IoGML
                              ]
    TOOL_PLUGINS: List[type] = [ToArrangeLinks, ToAscii, ToCDAutoLayout, ToFastEdit, ToLayout, ToLayoutSave,
                                ToOrthogonalLayoutV2, ToPython, ToSugiyama, ToTransforms
                                ]

    """
    Interface between the application and the plugins.

    Identifies all the know plugins
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

    def getInputPlugins(self) -> List[type]:
        """
        Get the input plugins.

        Returns:  A list of classes (the plugins classes).
        """

        pluginList = []
        for plug in self.IO_PLUGINS:
            obj = plug(None, None)
            if obj.getInputFormat() is not None:
                pluginList.append(plug)
        return pluginList

    def getOutputPlugins(self) -> List[type]:
        """
        Get the output plugins.

        Returns:  A list of classes (the plugins classes).
        """
        pluginList = []
        for plug in self.IO_PLUGINS:
            obj = plug(None, None)
            if obj.getOutputFormat() is not None:
                pluginList.append(plug)
        return pluginList

    def getToolPlugins(self) -> List[type]:
        """
        Get the tool plugins.

        Returns:    A list of classes (the plugins classes).
        """
        return self.TOOL_PLUGINS
