
from typing import TYPE_CHECKING
from typing import cast

from logging import Logger
from logging import getLogger

from pyutmodel.PyutText import PyutText

from ogl.OglText import OglText

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.wxcommands.BaseWxCommand import BaseWxCommand
from pyut.ui.wxcommands.BaseWxCommand import DoableClass

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class CommandCreateOglText(BaseWxCommand):

    def __init__(self, eventEngine: IEventEngine, x: int = 0, y: int = 0, oglText: OglText | None = None):

        self.logger: Logger = getLogger(__name__)

        super().__init__(canUndo=True, name='Create Text', eventEngine=eventEngine, x=x, y=y, oglObject=oglText)

    def _createNewObject(self) -> DoableClass:

        preferences: PyutPreferences = self._prefs

        pyutText: PyutText = PyutText(textContent=preferences.noteText)

        oglText: OglText       = OglText(pyutText)
        oglText.textFontFamily = preferences.textFontFamily
        oglText.textSize       = preferences.textFontSize
        oglText.isBold         = preferences.textBold
        oglText.isItalicized   = preferences.textItalicize

        return oglText

    def _placeShapeOnFrame(self):

        oglText:  OglText  = cast(OglText, self._shape)                 # get old
        pyutText: PyutText = cast(PyutText, oglText.pyutObject)
        #
        # Yet another reason to re-write miniogl.  I don't understand the model
        # stuff that it is maintaining;  However, I understand I have to recreate
        # the visuals so Shape._views is correct
        self._oglObjWidth, self._oglObjHeight = oglText.GetSize()
        self._shape = OglText(pyutText=pyutText, width=self._oglObjWidth, height=self._oglObjHeight)        # create new
        if self._invokeEditDialog is True:
            self._eventEngine.sendEvent(EventType.EditText, pyutText=pyutText)

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForAdd)

    def _cbGetActiveUmlFrameForAdd(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        self.logger.info(f'{umlFrame=}')
        oglText:  OglText  = cast(OglText, self._shape)

        umlFrame.addShape(oglText, self._oglObjX, self._oglObjY, withModelUpdate=True)

        umlFrame.Refresh()
