
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import EVT_BUTTON
from wx import EVT_CHECKBOX
from wx import VERTICAL

from wx import BoxSizer
from wx import Button
from wx import CheckBox
from wx import CommandEvent
from wx import Window

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _

from org.pyut.dialogs.preferences.PreferencesPanel import PreferencesPanel


class GeneralPreferencesPanel(PreferencesPanel):

    VERTICAL_GAP:   int = 5

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, parent: Window):

        super().__init__(parent=parent)

        [
            self.__autoResizeID, self.__showParamsID,
            self.__maximizeID,   self.__showTipsID,
            self.__resetTipsID,  self.__centerDiagramID
        ] = PyutUtils.assignID(6)

        self._createControls()
        self.__setControlValues()

    def _createControls(self):
        """
        Creates the main control and stashes them as private instance variables
        """

        self.__cbMaximize:      CheckBox = CheckBox(self, self.__maximizeID,      _("&Full Screen on startup"))
        self.__cbAutoResize:    CheckBox = CheckBox(self, self.__autoResizeID,    _("&Auto resize classes to fit content"))
        self.__cbShowParams:    CheckBox = CheckBox(self, self.__showParamsID,    _("&Show method parameters"))
        self.__cbShowTips:      CheckBox = CheckBox(self, self.__showTipsID,      _("Show &Tips on startup"))
        self.__cbCenterDiagram: CheckBox = CheckBox(self, self.__centerDiagramID, _('Center Diagram View'))

        self.__btnResetTips: Button = Button(self, self.__resetTipsID, _('Reset Tips'))

        mainSizer: BoxSizer = BoxSizer(VERTICAL)

        mainSizer.Add(self.__cbAutoResize,    0, ALL, GeneralPreferencesPanel.VERTICAL_GAP)
        mainSizer.Add(self.__cbShowParams,    0, ALL, GeneralPreferencesPanel.VERTICAL_GAP)
        mainSizer.Add(self.__cbMaximize,      0, ALL, GeneralPreferencesPanel.VERTICAL_GAP)
        mainSizer.Add(self.__cbCenterDiagram, 0, ALL, GeneralPreferencesPanel.VERTICAL_GAP)
        mainSizer.Add(self.__cbShowTips,      0, ALL, GeneralPreferencesPanel.VERTICAL_GAP)

        mainSizer.Add(self.__btnResetTips,   0, ALL, GeneralPreferencesPanel.VERTICAL_GAP)

        self.SetAutoLayout(True)
        self.SetSizer(mainSizer)

        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__autoResizeID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__showParamsID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__maximizeID)
        self.Bind(EVT_CHECKBOX, self.__OnCheckBox, id=self.__showTipsID)

        self.Bind(EVT_BUTTON,   self.__OnBtnResetTips, id=self.__resetTipsID)

    def __OnCheckBox(self, event: CommandEvent):
        """
        """
        self.__changed = True
        eventID = event.GetId()
        val = event.IsChecked()
        if eventID == self.__autoResizeID:
            self._prefs.autoResizeShapesOnEdit = val
        elif eventID == self.__showParamsID:
            self._mediator.showParams(val)
            self._prefs.showParameters = val
        elif eventID == self.__maximizeID:
            self._prefs.fullScreen = val
        elif eventID == self.__showTipsID:
            self._prefs.showTipsOnStartup = val
        else:
            self.clsLogger.warning(f'Unknown combo box ID: {eventID}')

    # noinspection PyUnusedLocal
    def __OnBtnResetTips(self, event: CommandEvent):
        # self._prefs[PyutPreferences.CURRENT_TIP] = '0'
        self._prefs.currentTip = 0

    def __setControlValues(self):
        """
        Set the default values on the controls.
        """
        self.__cbAutoResize.SetValue(self._prefs.autoResizeShapesOnEdit)
        self.__cbShowParams.SetValue(self._prefs.showParameters)
        self.__cbMaximize.SetValue(self._prefs.fullScreen)
        self.__cbShowTips.SetValue(self._prefs.showTipsOnStartup)

        self.__cbCenterDiagram.SetValue(self._prefs.centerDiagram)
