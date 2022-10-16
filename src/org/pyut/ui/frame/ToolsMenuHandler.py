
from logging import Logger
from logging import getLogger

from wx import CommandEvent
from wx import Menu

from wx import BeginBusyCursor
from wx import EndBusyCursor

from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin
from org.pyut.ui.frame.BaseMenuHandler import BaseMenuHandler


from org.pyut.PyutUtils import PyutUtils

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

from org.pyut.ui.tools.SharedTypes import PluginMap
from org.pyut.ui.tools.SharedTypes import ToolboxIdMap
from org.pyut.ui.tools.Tool import Category
from org.pyut.uiv2.ToolBoxHandler import ToolBoxHandler
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine


class ToolsMenuHandler(BaseMenuHandler):
    """
    Handles calling Tool plugins and I/O Plugins
    """
    def __init__(self, toolsMenu: Menu, toolPluginsMap: PluginMap, toolboxIds: ToolboxIdMap, eventEngine: IEventEngine = None):

        super().__init__(menu=toolsMenu, eventEngine=eventEngine)

        self.logger:          Logger       = getLogger(__name__)
        self._toolPluginsMap: PluginMap    = toolPluginsMap
        self._toolboxIds:     ToolboxIdMap = toolboxIds

    def onToolPlugin(self, event: CommandEvent):
        """

        Args:
            event:
        """
        wxId: int = event.GetId()
        self.logger.warning(f'{wxId=}')

        clazz: type = self._toolPluginsMap[wxId]
        # Create a plugin instance
        pluginInstance: PyutToPlugin = clazz(self._mediator.getUmlObjects(), self._mediator.activeUmlFrame)

        # Do plugin functionality
        BeginBusyCursor()
        try:
            pluginInstance.callDoAction()
            self.logger.debug(f"After tool plugin do action")
        except (ValueError, Exception) as e:
            PyutUtils.displayError(_("An error occurred while executing the selected plugin"), _("Error..."))
            self.logger.error(f'{e}')
        EndBusyCursor()

        # Refresh screen
        umlFrame = self._mediator.activeUmlFrame
        if umlFrame is not None:
            umlFrame.Refresh()

    def onToolboxMenuClick(self, event: CommandEvent):

        toolBoxHandler: ToolBoxHandler = ToolBoxHandler()

        # self._mediator.displayToolbox(self._toolboxIds[event.GetId()])
        toolBoxHandler.displayToolbox(Category(self._toolboxIds[event.GetId()]))
