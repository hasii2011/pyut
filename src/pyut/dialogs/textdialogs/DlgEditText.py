
from wx import EVT_TEXT
from wx import TE_MULTILINE

from wx import CommandEvent
from wx import TextCtrl
from wx import Window

from wx.lib.sized_controls import SizedPanel

from pyut.dialogs.textdialogs.BaseDlgEditText import BaseDlgEditText

from pyutmodel.PyutText import PyutText

from pyut.uiv2.eventengine.IEventEngine import IEventEngine


class DlgEditText(BaseDlgEditText):
    """
    Defines a multi-line text control dialog for placing an editable
    text on the UML Diagram


    Sample use:
        with DlgEditText(parent=self._frame, eventEngine=self._eventEngine, pyutText=pyutText) as dlg:

            if dlg.ShowModal() == OK:
                return f'Retrieved data: {pyutText.content=}'
            else:
                return f'Cancelled'

    """
    def __init__(self, parent: Window, eventEngine: IEventEngine, pyutText: PyutText):
        """

        Args:
            parent:             parent window to center on
            eventEngine
            pyutText:           Model object we are editing
        """
        super().__init__(parent, eventEngine=eventEngine, title='Diagram Text')

        sizedPanel: SizedPanel = self.GetContentsPane()

        self.pyutText: PyutText = pyutText

        self._txtCtrl: TextCtrl = TextCtrl(sizedPanel, value=self.pyutText.content, style=TE_MULTILINE)
        self._txtCtrl.SetSizerProps(expand=True, proportion=1)
        self._txtCtrl.SetFocus()

        self._createStandardOkCancelButtonSizer()

        self.Bind(EVT_TEXT, self._onTextLineChange, self._txtCtrl)

        self.Centre()

    def _onTextLineChange(self, event: CommandEvent):
        """
        Handle changes to the text in the widget identified by TXT_NOTE

        Args:
            event:
        """
        self.pyutText.content = event.GetString()
        self._markCurrentDiagramAsModified()
