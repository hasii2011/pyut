
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


class ToolsMenuHandler(BaseMenuHandler):
    """
    Handles calling Tool plugins and I/O Plugins
    """
    def __init__(self, toolsMenu: Menu, toolPluginsMap: PluginMap, toolboxIds: ToolboxIdMap):

        super().__init__(menu=toolsMenu)

        self.logger:          Logger       = getLogger(__name__)
        self._toolPluginsMap: PluginMap    = toolPluginsMap
        self._toolboxIds:     ToolboxIdMap = toolboxIds

    def onToolPlugin(self, event: CommandEvent):
        """

        Args:
            event:
        """
        # Create a plugin instance
        wxId: int = event.GetId()
        self.logger.warning(f'{wxId=}')

        clazz:          type         = self._toolPluginsMap[wxId]
        pluginInstance: PyutToPlugin = clazz(self._mediator.getUmlObjects(), self._mediator.getUmlFrame())

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
        umlFrame = self._mediator.getUmlFrame()
        if umlFrame is not None:
            umlFrame.Refresh()

    def onToolboxMenuClick(self, event: CommandEvent):
        self._mediator.displayToolbox(self._toolboxIds[event.GetId()])
