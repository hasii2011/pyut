from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from pkg_resources import resource_filename

from wx import BITMAP_TYPE_PNG
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_BUTTON
from wx import EVT_CHOICE
from wx import ICON_INFORMATION
from wx import ID_ANY

from wx import App
from wx import MessageDialog
from wx import OK
from wx import Point
from wx import Bitmap
from wx import Choice
from wx import Colour
from wx import CommandEvent

from wx.lib import colourdb

from wx.lib.buttons import GenBitmapTextButton

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel


from org.pyut.model.PyutClass import PyutClass

from org.pyut.ogl.OglClass import OglClass

from org.pyut.ogl.events.OglEventEngine import OglEventEngine
from org.pyut.ogl.events.OglEvents import EVT_SHAPE_SELECTED
from org.pyut.ogl.events.OglEvents import ShapeSelectedEvent
from org.pyut.ogl.events.ShapeSelectedEventData import ShapeSelectedEventData

from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

WINDOW_WIDTH:  int = 900
WINDOW_HEIGHT: int = 500


class TestOglEventEngine(App):

    def OnInit(self):

        PyutPreferences.determinePreferencesLocation()

        TestBase.setUpLogging()

        self.logger: Logger = getLogger(__name__)

        self._sizedFrame: SizedFrame = SizedFrame(parent=None, id=ID_ANY, title='Test OglEvent Engine', style=DEFAULT_FRAME_STYLE)

        self._setupTheUI(sizedFrame=self._sizedFrame)

        self._eventManager: OglEventEngine = OglEventEngine(listeningWindow=self._sizedFrame)

        self._eventManager.registerListener(EVT_SHAPE_SELECTED, self._onAShapeWasSelected)

        return True

    def _setupTheUI(self, sizedFrame: SizedFrame):

        sizedFrame.SetBackgroundColour(Colour(red=79, green=148, blue=205))
        sizedPanel:  SizedPanel = sizedFrame.GetContentsPane()
        sizedPanel.SetSizerType('vertical')

        b1: GenBitmapTextButton = self._createButton(parentPanel=sizedPanel, label='Select Shape', imageFileName='ShapeSelected.png')
        b2: GenBitmapTextButton = self._createButton(parentPanel=sizedPanel, label='Cut Ogl Class', imageFileName='CutOglClass.png')
        b3: GenBitmapTextButton = self._createButton(parentPanel=sizedPanel, label='Request Lollipop Location', imageFileName='RequestLollipopLocation.png')

        self._createBackGroundColorSelector(sizedFrame, sizedPanel)
        self.Bind(EVT_BUTTON, self._onSendShapeSelected, b1)
        self.Bind(EVT_BUTTON, self._onSendCutOglClassShape, b2)
        self.Bind(EVT_BUTTON, self._onSendRequestLollipopLocation, b3)

        sizedFrame.Show(True)

    def _createButton(self, parentPanel: SizedPanel, label: str, imageFileName: str) -> GenBitmapTextButton:

        fqFileName: str    = resource_filename(TestBase.RESOURCES_TEST_IMAGES_PACKAGE_NAME, imageFileName)
        selectPng:  Bitmap = Bitmap(fqFileName, BITMAP_TYPE_PNG)

        button: GenBitmapTextButton = GenBitmapTextButton(parentPanel, ID_ANY, None, label)
        button.SetBitmapLabel(selectPng)

        return button

    def _createBackGroundColorSelector(self, sizedFrame: SizedFrame, sizedPanel: SizedPanel):
        colourdb.updateColourDB()
        # create a colour list from the  database
        colour_list = colourdb.getColourList()

        # create a choice widget
        self._choice: Choice = Choice(sizedPanel, ID_ANY, choices=colour_list)
        # select item 0 (first item) in choice list to show
        self._choice.SetSelection(0)
        # set the current frame colour to the choice
        sizedFrame.SetBackgroundColour(self._choice.GetStringSelection())
        # bind the checkbox events to an action
        self._choice.Bind(EVT_CHOICE, self._onChoice)

    # noinspection PyUnusedLocal
    def _onSendShapeSelected(self, event: CommandEvent):

        pyutClass: PyutClass = PyutClass(name='TestShape')
        oglClass:  OglClass  = OglClass(pyutClass=pyutClass)
        self._eventManager.sendSelectedShapeEvent(shape=oglClass, position=Point(100, 100))

    def _onSendCutOglClassShape(self, event: CommandEvent):
        self.logger.info(f'{event=}')

    def _onSendRequestLollipopLocation(self, event: CommandEvent):
        self.logger.info(f'{event=}')

    def _onAShapeWasSelected(self, event: ShapeSelectedEvent):

        shapeSelectedData: ShapeSelectedEventData = event.shapeSelectedData
        msg: str = f'{shapeSelectedData.shape}{osLineSep}position{shapeSelectedData.position}'
        dlg: MessageDialog = MessageDialog(self._sizedFrame, msg, 'Success', OK | ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    # noinspection PyUnusedLocal
    def _onChoice(self, event):
        bgColor = self._choice.GetStringSelection()
        # change colour of the panel to the selected colour ...
        self._sizedFrame.SetBackgroundColour(bgColor)
        self._sizedFrame.Refresh()


testApp: App = TestOglEventEngine(redirect=False)

testApp.MainLoop()
