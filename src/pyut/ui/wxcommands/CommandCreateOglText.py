
from typing import TYPE_CHECKING
from typing import cast

from logging import Logger
from logging import getLogger

from pyutmodel.PyutText import PyutText

from ogl.OglText import OglText

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.wxcommands.BaseWxCreateCommand import BaseWxCreateCommand
from pyut.ui.wxcommands.Types import DoableObjectType

from pyut.uiv2.eventengine.Events import EventType
from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class CommandCreateOglText(BaseWxCreateCommand):

    def __init__(self, x: int, y: int, eventEngine: IEventEngine):

        self.logger: Logger = getLogger(__name__)

        super().__init__(canUndo=True, name='Create Text', x=x, y=y, eventEngine=eventEngine)

    def _createPrototypeInstance(self) -> DoableObjectType:

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

        self._eventEngine.sendEvent(EventType.EditText, pyutText=pyutText)

        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForAdd)

    def _cbGetActiveUmlFrameForAdd(self, frame: 'UmlDiagramsFrame'):

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        self.logger.info(f'{umlFrame=}')
        oglText:  OglText  = cast(OglText, self._shape)

        umlFrame.addShape(oglText, self._oglObjX, self._oglObjY, withModelUpdate=True)

        umlFrame.Refresh()
