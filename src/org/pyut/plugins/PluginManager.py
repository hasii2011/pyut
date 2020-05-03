
from typing import List

from logging import Logger
from logging import getLogger

from os import sep as osSep

from org.pyut.general.Singleton import Singleton

from org.pyut.plugins.IoCpp import IoCpp
from org.pyut.plugins.IoDTD import IoDTD
from org.pyut.plugins.IoJava import IoJava
from org.pyut.plugins.IoJavaReverse import IoJavaReverse
from org.pyut.plugins.IoJavascript import IoJavascript
from org.pyut.plugins.IoPython import IoPython
from org.pyut.plugins.IoXmi import IoXmi
from org.pyut.plugins.IoXmi_OMG import IoXmi_OMG
from org.pyut.plugins.IoXml import IoXml
from org.pyut.plugins.IoXSD import IoXSD

from org.pyut.plugins.ToArrangeLinks import ToArrangeLinks
from org.pyut.plugins.ToAscii import ToAscii
from org.pyut.plugins.ToCDAutoLayout import ToCDAutoLayout
from org.pyut.plugins.ToFastEdit import ToFastEdit
from org.pyut.plugins.ToLayout import ToLayout
from org.pyut.plugins.ToLayoutSave import ToLayoutSave
from org.pyut.plugins.ToOrthogonalLayout import ToOrthogonalLayout
from org.pyut.plugins.ToPython import ToPython
from org.pyut.plugins.ToSugiyama import ToSugiyama
from org.pyut.plugins.ToTransforms import ToTransforms

FileNameListType = List[str]


class PluginManager(Singleton):

    PLUGIN_DIRECTORY: str = f"org{osSep}pyut{osSep}plugins"
    PLUGIN_PACKAGE:   str = 'org.pyut.plugins'

    ioPlugs: List[type] = [IoCpp, IoDTD, IoJava, IoJavaReverse, IoJavascript,
                           IoPython, IoXmi, IoXmi_OMG, IoXml, IoXSD
                           ]
    toPlugs: List[type] = [ToArrangeLinks, ToAscii, ToCDAutoLayout, ToFastEdit, ToLayout, ToLayoutSave,
                           ToOrthogonalLayout, ToPython, ToSugiyama, ToTransforms
                           ]

    """
    Interface between the application and the plugins.

    Identifies all the know plugins
    """
    def init(self):
        """
        Singleton Constructor.
        """
        self.logger:  Logger     = getLogger(__name__)

    def getPluginsInfo(self) -> List[str]:
        """
        Get textual information about available plugins.

        Returns:  A string list
        """
        s: List[str] = []
        for plug in self.ioPlugs + self.toPlugs:
            obj = plug(None, None)
            s.append(f"Plugin : {obj.getName()} version {obj.getVersion()} (c) by {obj.getAuthor()}")
        return s

    def getInputPlugins(self) -> List[type]:
        """
        Get the input plugins.

        Returns:  A list of classes (the plugins classes).
        """

        pluginList = []
        for plug in self.ioPlugs:
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
        for plug in self.ioPlugs:
            obj = plug(None, None)
            if obj.getOutputFormat() is not None:
                pluginList.append(plug)
        return pluginList

    def getToolPlugins(self) -> List[type]:
        """
        Get the tool plugins.

        Returns:    A list of classes (the plugins classes).
        """
        return self.toPlugs
