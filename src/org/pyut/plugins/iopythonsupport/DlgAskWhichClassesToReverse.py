
from wx import CAPTION
from wx import CommandEvent
from wx import EVT_BUTTON
from wx import EXPAND
from wx import HORIZONTAL
from wx import ID_CANCEL
from wx import LB_ALWAYS_SB
from wx import LB_EXTENDED
from wx import LB_SORT
from wx import RESIZE_BORDER
from wx import VERTICAL
from wx import ID_ANY
from wx import ID_OK

from wx import ListBox
from wx import StaticText
from wx import BoxSizer
from wx import Dialog
from wx import Button

from org.pyut.PyutUtils import PyutUtils

from org.pyut.general.Globals import _

[ID_BTN_TO_THE_RIGHT, ID_BTN_TO_THE_LEFT] = PyutUtils.assignID(2)


class DlgAskWhichClassesToReverse(Dialog):

    def __init__(self, lstClasses):

        super().__init__(None, ID_ANY, "Classes choice", style=CAPTION | RESIZE_BORDER, size=(400, 500))

        # Create not chosen classes listBox
        self._listBox1 = ListBox(self, ID_ANY, style=LB_EXTENDED | LB_ALWAYS_SB | LB_SORT, size=(320, 400))
        for klass in lstClasses:
            self._listBox1.Append(klass.__name__, klass)

        # Create chosen classes listBox
        self._listBox2 = ListBox(self, ID_ANY, style=LB_EXTENDED | LB_ALWAYS_SB | LB_SORT, size=(320, 400))

        # Create buttons
        btnOk = Button(self, ID_OK, "Ok")
        btnToTheRight = Button(self, ID_BTN_TO_THE_RIGHT, "=>")
        btnToTheLeft  = Button(self, ID_BTN_TO_THE_LEFT,  "<=")

        # Callbacks
        self.Bind(EVT_BUTTON, self._onBtnToTheRight, id=ID_BTN_TO_THE_RIGHT)
        self.Bind(EVT_BUTTON, self._onBtnToTheLeft,  id=ID_BTN_TO_THE_LEFT)

        # Create info label
        lblChoice = StaticText(self, ID_ANY, _("Choose classes to reverse: "))

        # Create buttons sizer
        szrBtn = BoxSizer(VERTICAL)
        szrBtn.Add(btnToTheRight, 0, EXPAND)
        szrBtn.Add(btnToTheLeft,  0, EXPAND)

        # Create lists and buttons sizer
        szrLB = BoxSizer(HORIZONTAL)
        szrLB.Add(self._listBox1,  0, EXPAND)
        szrLB.Add(szrBtn,          0, EXPAND)
        szrLB.Add(self._listBox2,  0, EXPAND)

        # Create sizer
        box = BoxSizer(VERTICAL)
        box.Add(lblChoice, 0, EXPAND)
        box.Add(szrLB,     0, EXPAND)
        box.Add(btnOk,     0, EXPAND)
        box.Fit(self)
        self.SetAutoLayout(True)
        self.SetSizer(box)

        # Show dialog
        self.ShowModal()
        if self.GetReturnCode() == ID_CANCEL:     # abort -> empty right column

            while self._listBox2.GetCount() > 0:
                data = self._listBox2.GetClientData(0)
                name = self._listBox2.GetString(0)
                self._listBox1.Append(name, data)
                self._listBox2.Delete(0)

    def getChosenClasses(self):
        """
        Return the classes chosen by the user
        """
        ret = []
        for el in range(self._listBox2.GetCount()):
            ret.append(self._listBox2.GetClientData(el))
        return ret

    # noinspection PyUnusedLocal
    def _onBtnToTheRight(self, event: CommandEvent):
        """
        Callback for the "=>" button
        """
        lst = list(self._listBox1.GetSelections())
        lst.sort()
        lst.reverse()
        for i in lst:
            data = self._listBox1.GetClientData(i)
            name = self._listBox1.GetString(i)
            self._listBox2.Append(name, data)
            self._listBox1.Delete(i)

    # noinspection PyUnusedLocal
    def _onBtnToTheLeft(self, event: CommandEvent):
        """
        Callback for the "<=" button
        """
        lst = list(self._listBox2.GetSelections())
        lst.sort()
        lst.reverse()
        for i in lst:
            data = self._listBox2.GetClientData(i)
            name = self._listBox2.GetString(i)
            self._listBox1.Append(name, data)
            self._listBox2.Delete(i)
