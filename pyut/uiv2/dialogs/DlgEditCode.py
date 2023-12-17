
from os import linesep as osLineSep

from wx import BOTH
from wx import CANCEL
from wx import CAPTION
from wx import CLOSE_BOX
from wx import CommandEvent
from wx import DIALOG_EX_METAL
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import EVT_TEXT
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK
from wx import Size

from wx import TE_MULTILINE
from wx import TextCtrl

from wx.lib.sized_controls import SizedDialog

from wx import NewIdRef as wxNewIdRef
from wx.lib.sized_controls import SizedPanel

from pyutmodelv2.PyutMethod import SourceCode

TXT_CODE: int = wxNewIdRef()


class DlgEditCode(SizedDialog):
    """
    Dialog for the class comment edition.
    """

    def __init__(self, parent, wxID, sourceCode: SourceCode):
        """
        We'll modify pyutMethod on OK
        Args:
            parent:
            wxID:
            sourceCode:
        """
        self._sourceCode:            SourceCode = sourceCode
        self._displayableSourceCode: str        = f'{osLineSep}'.join(sourceCode)

        super().__init__(parent, wxID, 'Method Code', style=CAPTION | CLOSE_BOX | DIALOG_EX_METAL)

        self.Center(BOTH)
        panel: SizedPanel = self.GetContentsPane()

        panel.SetSizerType('vertical')

        self._txtCtrl: TextCtrl = TextCtrl(panel, TXT_CODE, self._displayableSourceCode, style=TE_MULTILINE)

        self._txtCtrl.SetSizerProps(expand=True)
        print(f'{self._txtCtrl.GetSize()=}')

        txtCtrlSize: Size = self._txtCtrl.GetSize()
        newSize:     Size = Size()
        newSize.SetWidth(txtCtrlSize.GetWidth() * 4)
        newSize.SetHeight(txtCtrlSize.GetHeight())
        self._txtCtrl.SetMinSize(newSize)

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(OK | CANCEL))

        self.Fit()
        self.SetMinSize(self.GetSize())

        self.Bind(EVT_TEXT,   self.__onSourceCodeChange, id=TXT_CODE)
        self.Bind(EVT_BUTTON, self.__onCmdOk, id=ID_OK)
        self.Bind(EVT_BUTTON, self.__onClose, id=ID_CANCEL)
        self.Bind(EVT_CLOSE,  self.__onClose)

    @property
    def sourceCode(self) -> SourceCode:
        return self._sourceCode

    def __onSourceCodeChange(self, event: CommandEvent):
        self._displayableSourceCode = event.GetString()

    # noinspection PyUnusedLocal
    def __onCmdOk(self, event: CommandEvent):
        """
        """
        self._sourceCode = SourceCode(self._displayableSourceCode.split(osLineSep))
        self.SetReturnCode(OK)       # TODO Fix this;  should be OK
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def __onClose(self, event: CommandEvent):
        """
        """
        self.SetReturnCode(CANCEL)      # This is correct
        self.EndModal(ID_CANCEL)
