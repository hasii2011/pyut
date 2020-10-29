
from typing import cast

from logging import Logger
from logging import getLogger

from sys import exit as sysExit

from wx import DEFAULT_FRAME_STYLE
from wx import ID_ANY
from wx import OK

from wx import App
from wx import Frame

from org.pyut.model.PyutModifier import PyutModifier
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.general.Mediator import Mediator

from org.pyut.model.PyutMethod import PyutMethod

from org.pyut.dialogs.DlgEditMethod import DlgEditMethod

from tests.TestBase import TestBase

from unittest.mock import MagicMock


class TestADialog(App):

    FRAME_ID: int = ID_ANY

    def OnInit(self):

        TestBase.setUpLogging()
        self.logger: Logger = getLogger(__name__)
        frameTop:    Frame = Frame(parent=None, id=TestADialog.FRAME_ID, title="Test A Dialog", size=(600, 400), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(False)

        PyutPreferences.determinePreferencesLocation()

        self.SetTopWindow(frameTop)

        self._frameTop = frameTop
        self._preferences: PyutPreferences = PyutPreferences()
        #
        # Introduce a mock
        #
        fileHandler = MagicMock()
        self._mediator = Mediator()
        self._mediator.registerFileHandling(fileHandler)
        self.initTest()
        return True

    def initTest(self):

        pyutMethod: PyutMethod = PyutMethod(name='TestMethod')
        pyutMethod.visibility = PyutVisibilityEnum.PRIVATE
        pyutMethod.returnType = PyutType('float')
        pyutMethod._modifiers = [PyutModifier('abstract')]

        pyutParam: PyutParam = PyutParam(name='param1')
        pyutParam.type         = PyutType(value='str')
        pyutParam.defaultValue = 'bogus'

        pyutMethod.parameters = [pyutParam]

        with DlgEditMethod(theParent=self._frameTop, theWindowId=ID_ANY, methodToEdit=pyutMethod, theMediator=self._mediator) as dlg:
            dlg: DlgEditMethod = cast(DlgEditMethod, dlg)
            if dlg.ShowModal() == OK:
                # self.logger.warning(f'Retrieved data: layoutWidth: {dlg.layoutWidth} layoutHeight: {dlg.layoutHeight}')
                self._frameTop.Close(force=True)
                self.logger.warning(f'{self._preferences.centerDiagram=}')

            else:
                self.logger.warning(f'Cancelled')
                self._frameTop.Close(force=True)

        self.logger.info(f"After dialog show")
        sysExit()   # brutal !!


testApp: App = TestADialog(redirect=False)

testApp.MainLoop()
