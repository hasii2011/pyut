
from logging import Logger
from logging import getLogger

from wx import CommandEvent
from wx import Menu

from pyutplugins.PluginManager import PluginManager
from pyutplugins.IPluginAdapter import IPluginAdapter

from pyut.ui.frame.BaseMenuHandler import BaseMenuHandler

from pyut.ui.tools.SharedTypes import ToolboxIdMap
from pyut.ui.tools.Tool import Category

from pyut.uiv2.PluginAdapter import PluginAdapter
from pyut.uiv2.ToolBoxHandler import ToolBoxHandler

from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class ToolsMenuHandler(BaseMenuHandler):
    """
    Handles calling Tool plugins and I/O Plugins
    """
    def __init__(self, toolsMenu: Menu, pluginManager: PluginManager, toolboxIds: ToolboxIdMap, eventEngine: IEventEngine):

        super().__init__(menu=toolsMenu, eventEngine=eventEngine)

        self.logger:          Logger       = getLogger(__name__)
        self._pluginManager: PluginManager = pluginManager
        # self._toolPluginsMap: PluginIDMap  = toolPluginsMap
        self._toolboxIds:     ToolboxIdMap = toolboxIds

        self._pluginAdapter:  IPluginAdapter = PluginAdapter(eventEngine=eventEngine)

    def onToolPlugin(self, event: CommandEvent):
        """

        Args:
            event:
        """
        wxId: int = event.GetId()
        self.logger.debug(f'{wxId=}')
        self._pluginManager.doToolAction(wxId=wxId)

    def onToolboxMenuClick(self, event: CommandEvent):

        toolBoxHandler: ToolBoxHandler = ToolBoxHandler()

        # self._mediator.displayToolbox(self._toolboxIds[event.GetId()])        # TODO
        toolBoxHandler.displayToolbox(Category(self._toolboxIds[event.GetId()]))
