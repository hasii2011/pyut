
from os import getcwd
from os import path as osPath
from os import sep as osSeparator

from wx import ALL
from wx import BOTH
from wx import BOTTOM
from wx import EVT_BUTTON
from wx import GROW
from wx import HORIZONTAL
from wx import ID_OK
from wx import VERTICAL

from wx import Dialog
from wx import MessageBox
from wx import Size
from wx import BoxSizer
from wx import Button
from wx import DefaultPosition

from wx.html import HtmlWindow
from wx.html import HtmlEasyPrinting

from wx.lib.dialogs import ScrolledMessageDialog

from pyutUtils import assignID

from globals import _

[ID_LOAD_FILE, ID_BACK, ID_FORWARD, ID_PRINT, ID_VIEW_SOURCE] = assignID(5)


class DlgHelp(Dialog):
    """
    Pyut help dialog frame. Used to show help and navigate through it.

    To use it from a wxFrame :
        dlg = DlgHelp(self, -1, "Pyut Help")
        dlg.Show()
        dlg.destroy()

    :version: $Revision: 1.7 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """
    def __init__(self, parent, ID, title):
        """
        Constructor.

        @since 1.0
        @author C.Dutoit
        """
        # dialog box
        super().__init__(parent, ID, title, DefaultPosition, Size(720, 520))

        self.Center(BOTH)

        self.html = HtmlWindow(self, -1, DefaultPosition, Size(720, 520))
        #
        # TODO Change this to load as a resource
        #
        self.html.LoadPage(getcwd() + osSeparator + "help" + osSeparator + "index.html")

        self.printer = HtmlEasyPrinting()

        self.box = BoxSizer(VERTICAL)
        self.box.Add(self.html, 1, GROW)
        subbox = BoxSizer(HORIZONTAL)

        btn = Button(self, ID_BACK, _("Back"))
        self.Bind(EVT_BUTTON, self.__OnBack, id=ID_BACK)
        subbox.Add(btn, 1, GROW | ALL, 2)

        btn = Button(self, ID_FORWARD, _("Forward"))
        self.Bind(EVT_BUTTON, self.__OnForward, id=ID_FORWARD)
        subbox.Add(btn, 1, GROW | ALL, 2)

        btn = Button(self, ID_PRINT, _("Print"))
        self.Bind(EVT_BUTTON, self.__OnPrint, id=ID_PRINT)
        subbox.Add(btn, 1, GROW | ALL, 2)

        btn = Button(self, ID_VIEW_SOURCE, _("View Source"))
        self.Bind(EVT_BUTTON, self.__OnViewSource, id=ID_VIEW_SOURCE)
        subbox.Add(btn, 1, GROW | ALL, 2)

        btn = Button(self, ID_OK, _("Exit"))
        subbox.Add(btn, 1, GROW | ALL, 2)

        self.box.Add(subbox, 0, GROW | BOTTOM)
        self.SetSizer(self.box)
        self.SetAutoLayout(True)
        subbox.Fit(self)
        self.box.Fit(self)

        self.OnShowDefault(None)

        self.Show(True)

    def OnShowDefault(self, event):
        """
        Show default page

        @since 1.1
        @author C.Dutoit
        """
        name = osPath.join(getcwd(), 'help/index.html')
        self.html.LoadPage(name)

    # def __OnLoadFile(self, event):
        # """
        # Load a html page
#
        # @since 1.1
        # @author C.Dutoit
        # """
        # dlg = wx.FileDialog(self, wildcard = '*.htm*', style=wx.OPEN)
        # if dlg.ShowModal()==wx.OK:
            # path = dlg.GetPath()
            # self.html.LoadPage(path)
        # dlg.Destroy()

    def __OnBack(self, event):
        """
        go one level back; load last page

        @since 1.1
        @author C.Dutoit
        """
        if not self.html.HistoryBack():
            MessageBox(_("No more items in history !"))

    def __OnForward(self, event):
        """
        go one level forward; load next page

        @since 1.1
        @author C.Dutoit
        """
        if not self.html.HistoryForward():
            MessageBox(_("No more items in history !"))

    def __OnViewSource(self, event):
        """
        View document source

        @since 1.1
        @author C.Dutoit
        """
        #  from wx.Python.lib.dialogs import ScrolledMessageDialog
        source = self.html.GetParser().GetSource()
        dlg = ScrolledMessageDialog(self, source, _('HTML Source'))
        dlg.ShowModal()
        dlg.Destroy()

    def __OnPrint(self, event):
        """
        print the current page

        @since 1.1
        @author C.Dutoit
        """
        self.printer.PrintFile(self.html.GetOpenedPage())
