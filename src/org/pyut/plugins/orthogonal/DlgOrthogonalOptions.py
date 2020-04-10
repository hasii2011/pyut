
from logging import Logger
from logging import getLogger

from wx import ALL
from wx import CANCEL
from wx import CENTER
from wx import EVT_BUTTON
from wx import EVT_CHECKBOX
from wx import EVT_CLOSE
from wx import EVT_RADIOBOX
from wx import EVT_SPINCTRL
from wx import EXPAND
from wx import OK
from wx import RA_SPECIFY_COLS
from wx import RadioBox
from wx import SpinEvent
from wx import VERTICAL
from wx import HORIZONTAL
from wx import ID_OK
from wx import ID_ANY

from wx import CommandEvent
from wx import DefaultPosition
from wx import DefaultSize

from wx import BoxSizer
from wx import StaticBoxSizer

from wx import CheckBox
from wx import SpinCtrl
from wx import StaticBox
from wx import Button
from wx import StaticText
from wx import Dialog

from org.pyut.plugins.orthogonal.OrthogonalOrientation import OrthogonalOrientation
from org.pyut.plugins.orthogonal.OrthogonalOptions import OrthogonalOptions

from org.pyut.general.Globals import _

from org.pyut.PyutUtils import PyutUtils


class DlgOrthogonalOptions(Dialog):

    HORIZONTAL_GAP:        int = 5
    VERTICAL_GAP:          int = 3
    SPINNER_CONTAINER_GAP: int = 2

    def __init__(self, parent):
        """
        """
        super().__init__(parent, ID_ANY, _("Orthogonal Options"))
        self.logger: Logger = getLogger(__name__)

        self.__initializeTheControls()

        self.options:   OrthogonalOptions = OrthogonalOptions()
        self.__changed: bool              = False
        self.__setValues()

        self.Bind(EVT_CLOSE, self.__OnClose)

    def __initializeTheControls(self):
        """
        Initialize the controls.
        """
        # IDs
        [
            self.__compactLayoutId, self.__layerSpacingId, self.__nodeSpacingId, self.__orientationId
        ] = PyutUtils.assignID(4)

        self.__createMainControls()

        hs:        BoxSizer = self.__createDialogButtonsContainer()
        box:       StaticBox = StaticBox(self, ID_ANY, "")
        mainSizer: StaticBoxSizer = StaticBoxSizer(box, VERTICAL)

        mainSizer.Add(self.__compactLayout, 0, ALL, DlgOrthogonalOptions.VERTICAL_GAP)
        layerSpacingSizer: BoxSizer = self.__createSpinnerContainer(self.__scLayerSpacing, _('Layer Spacing'))
        nodeSpacingSizer:  BoxSizer = self.__createSpinnerContainer(self.__scNodeSpacing,  _('Node Spacing'))

        mainSizer.Add(layerSpacingSizer, 0, ALL, DlgOrthogonalOptions.VERTICAL_GAP)
        mainSizer.Add(nodeSpacingSizer,  0, ALL, DlgOrthogonalOptions.VERTICAL_GAP)

        self.__createOrientationControl()

        mainSizer.Add(self.__rbOrientation, 0, ALL, DlgOrthogonalOptions.VERTICAL_GAP)
        mainSizer.Add(hs, 0, CENTER)

        border: BoxSizer = BoxSizer()
        border.Add(mainSizer, 1, EXPAND | ALL, 3)

        self.SetAutoLayout(True)
        self.SetSizer(border)

        border.Fit(self)
        border.SetSizeHints(self)

        self.Bind(EVT_CHECKBOX, self.__OnCompactLayoutChange, id=self.__compactLayoutId)
        self.Bind(EVT_RADIOBOX, self._onOrientationChange,    id=self.__orientationId)
        self.Bind(EVT_SPINCTRL, self.__OnSpacingChange,       id=self.__layerSpacingId)
        self.Bind(EVT_SPINCTRL, self.__OnSpacingChange,       id=self.__nodeSpacingId)

        self.Bind(EVT_BUTTON,   self.__OnCmdOk,    id=ID_OK)

    def __createMainControls(self):
        """
        Creates the main control and stashes them as private instance variables
        """
        self.__compactLayout: CheckBox = CheckBox(self, self.__compactLayoutId,  _("&Do compact layout"))

        scLayerSpacing = SpinCtrl(self, self.__layerSpacingId, "", (30, 50))
        scNodeSpacing  = SpinCtrl(self, self.__nodeSpacingId,      "", (30, 50))

        scLayerSpacing.SetRange(10, 100)
        scNodeSpacing.SetRange(10, 100)
        self.__scLayerSpacing  = scLayerSpacing
        self.__scNodeSpacing      = scNodeSpacing

    def __createDialogButtonsContainer(self) -> BoxSizer:

        hs: BoxSizer = BoxSizer(HORIZONTAL)

        btnOk: Button = Button(self, ID_OK, _("&OK"))
        hs.Add(btnOk, 0, ALL, DlgOrthogonalOptions.SPINNER_CONTAINER_GAP)
        return hs

    def __createSpinnerContainer(self, spinner: SpinCtrl, text: str) -> BoxSizer:

        lblText = StaticText(self, ID_ANY, text)

        szrSpinner = BoxSizer(HORIZONTAL)
        szrSpinner.Add(lblText, 0, ALL, DlgOrthogonalOptions.HORIZONTAL_GAP)
        szrSpinner.Add(spinner, 0, ALL, DlgOrthogonalOptions.HORIZONTAL_GAP)

        return szrSpinner

    def __createOrientationControl(self):

        orientationOptions = [OrthogonalOrientation.VERTICAL.value, OrthogonalOrientation.HORIZONTAL.value]

        rb: RadioBox = RadioBox(
            self, self.__orientationId, _('Layout Orientation'), DefaultPosition, DefaultSize,
            orientationOptions, 2, RA_SPECIFY_COLS
        )
        self.__rbOrientation = rb

    def __setValues(self):
        """
        Set the default values to the controls.
        """
        self.__compactLayout.SetValue(self.options.compactLayout)
        self.__scLayerSpacing.SetValue(self.options.layerSpacing)
        self.__scNodeSpacing.SetValue(self.options.nodeSpacing)

    def __OnCompactLayoutChange(self, event: CommandEvent):

        self.__changed = True
        eventID:  int  = event.GetId()
        newValue: bool = event.IsChecked()
        if eventID == self.__compactLayoutId:
            self.options.compactLayout = newValue
        else:
            self.logger.error(f'Unknown control ID: {eventID}')

    def _onOrientationChange(self, event: CommandEvent):

        orientation: OrthogonalOrientation = OrthogonalOrientation(event.GetString())
        self.options.orientation = orientation

    def __OnSpacingChange(self, event: SpinEvent):

        self.__changed = True
        eventId:  int = event.GetId()
        newValue: int = event.GetInt()

        if eventId == self.__layerSpacingId:
            self.options.layerSpacing = newValue
        elif eventId == self.__nodeSpacingId:
            self.options.nodeSpacing = newValue
        else:
            self.logger.error(f'Unknown spacing event id: {eventId}')

    def __OnCmdOk(self, event: CommandEvent):
        """
        """
        if self.__changed is True:
            self.logger.info(f'Preferences have changed')
        event.Skip(skip=True)
        self.SetReturnCode(OK)
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def __OnClose(self, event: CommandEvent):
        """
        """
        self.SetReturnCode(CANCEL)
        self.EndModal(CANCEL)
