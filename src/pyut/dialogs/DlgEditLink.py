
from logging import Logger
from logging import getLogger

from wx import ALIGN_CENTER_HORIZONTAL
from wx import ALIGN_CENTRE
from wx import ALIGN_LEFT
from wx import ALIGN_RIGHT
from wx import ALL
from wx import BOTTOM
from wx import BoxSizer
from wx import Button
from wx import CANCEL
from wx import CAPTION
from wx import CommandEvent
from wx import Dialog
from wx import EVT_BUTTON
from wx import EVT_TEXT
from wx import FlexGridSizer
from wx import GROW
from wx import HORIZONTAL
from wx import OK
from wx import RESIZE_BORDER
from wx import RIGHT
from wx import Size
from wx import StaticText
from wx import TextCtrl
from wx import VERTICAL

from org.pyut.PyutUtils import PyutUtils

from pyutmodel.PyutLink import PyutLink

# noinspection PyProtectedMember
from org.pyut.general.Globals import _

from copy import deepcopy


[
    TXT_CARDINALITY_A,
    TXT_CARDINALITY_B,
    TXT_RELATIONSHIP,
    A_ROLE_IN_B,
    B_ROLE_IN_A,
    BTN_REMOVE
] = PyutUtils.assignID(6)


class DlgEditLink (Dialog):
    """
    Dialog for the link (between classes) editing.

    to use it :
        dlg=DlgEditLink(...)
        dlg.setValues(...)
        dlg.ShowModal()

    to see if the user clicked on Ok or Cancel :
        x=dlg.getReturnAction()

    to get new values :
        x=dlg.getCardinality()
        x=dlg.getRoles()
        x=dlg.getRelationship()

    don't forget :
        dlg.Destroy()
    :version: $Revision: 1.9 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """

    def __init__(self, parent, ID, pyutLink: PyutLink):
        """
        """
        super().__init__(parent, ID, _("Link Edit"), style=RESIZE_BORDER | CAPTION)

        self.logger: Logger = getLogger(__name__)
        # Associated PyutLink
        self._pyutLink: PyutLink = pyutLink

        self._relationship = self._pyutLink.name
        self._aRoleInB = ""
        self._bRoleInA = ""
        # self._cardinalityA = self._pyutLink.getSourceCardinality()
        # self._cardinalityB = self._pyutLink.getDestinationCardinality()
        self._cardinalityA = self._pyutLink.sourceCardinality
        self._cardinalityB = self._pyutLink.destinationCardinality

        self._returnAction = CANCEL      # #describe how user exited dialog box

        #  labels
        lblCardA = StaticText(self, -1, _("Cardinality"),  style=ALIGN_LEFT)
        lblRela  = StaticText(self, -1, _("Relationship"), style=ALIGN_CENTRE)
        lblCardB = StaticText(self, -1, _("Cardinality"),  style=ALIGN_RIGHT)
        lblA     = StaticText(self, -1, "A",      style=ALIGN_LEFT)
        self._lblArrow = StaticText(self, -1, "", style=ALIGN_CENTRE)
        self.updateLblArrow()
        lblB     = StaticText(self, -1, "B",      style=ALIGN_RIGHT)
        lblAinB  = StaticText(self, -1, _("A's role in B"), style=ALIGN_LEFT)
        lblBinA  = StaticText(self, -1, _("B's role in A"), style=ALIGN_RIGHT)

        #  text
        self._txtCardinalityA = TextCtrl(self, TXT_CARDINALITY_A, "", size=Size(50, 20))
        self._txtRelationship = TextCtrl(self, TXT_RELATIONSHIP,  "", size=Size(100, 20))
        self._txtCardinalityB = TextCtrl(self, TXT_CARDINALITY_B, "", size=Size(50, 20))
        self._txtARoleB = TextCtrl(self, A_ROLE_IN_B, "")
        self._txtBRoleA = TextCtrl(self, B_ROLE_IN_A, "")

        self.setValues(self._relationship, self._aRoleInB, self._bRoleInA, self._cardinalityA, self._cardinalityB)

        self._txtARoleB.Enable(False)
        self._txtBRoleA.Enable(False)

        #  text events
        self.Bind(EVT_TEXT, self._onTxtCardinalityAChange, id=TXT_CARDINALITY_A)
        self.Bind(EVT_TEXT, self._onTxtCardinalityBChange, id=TXT_CARDINALITY_B)
        self.Bind(EVT_TEXT, self._onTxtRelationshipChange, id=TXT_RELATIONSHIP)
        self.Bind(EVT_TEXT, self._onTxtARoleBChange, id=A_ROLE_IN_B)
        self.Bind(EVT_TEXT, self._onTxtBRoleAChange, id=B_ROLE_IN_A)

        #  Ok/Cancel
        btnOk     = Button(self, OK, _("&Ok"))
        btnCancel = Button(self, CANCEL, _("&Cancel"))
        btnRemove = Button(self, BTN_REMOVE, _("&Remove"))
        btnOk.SetDefault()

        #  button events
        self.Bind(EVT_BUTTON, self._onCmdOk,     id=OK)
        self.Bind(EVT_BUTTON, self._onCmdCancel, id=CANCEL)
        self.Bind(EVT_BUTTON, self._onRemove,    id=BTN_REMOVE)

        szr1 = FlexGridSizer(cols=3, hgap=30, vgap=5)
        szr1.AddMany([
            (lblCardA, 0, ALIGN_LEFT),
            (lblRela,  0, ALIGN_CENTER_HORIZONTAL),
            (lblCardB, 0, ALIGN_RIGHT),
            (self._txtCardinalityA, 0, ALIGN_LEFT),
            (self._txtRelationship, 0, ALIGN_CENTER_HORIZONTAL),
            (self._txtCardinalityB, 0, ALIGN_RIGHT)])
        szr1.AddGrowableCol(0)
        szr1.AddGrowableCol(1)
        szr1.AddGrowableCol(2)

        szr2 = BoxSizer(HORIZONTAL)
        szr2.Add(lblA, 1, GROW | RIGHT, 10)
        szr2.Add(self._lblArrow, 1, GROW, 10)
        szr2.Add(lblB, 1, GROW)

        # szr3 :
        #        lblAinB,         lblBinA
        #        self._txtARoleB, self._txtBRoleA
        szr3 = FlexGridSizer(cols=2, hgap=30, vgap=5)
        szr3.AddMany([
            (lblAinB, 0),
            (lblBinA, 0, ALIGN_RIGHT),
            (self._txtARoleB, 0),
            (self._txtBRoleA, 0, ALIGN_RIGHT | BOTTOM, 20)])
        szr3.AddGrowableCol(0)
        szr3.AddGrowableCol(1)

        # szr4 :
        #        btnRemove, btnOk, btnCancel
        szr4 = BoxSizer(HORIZONTAL)
        szr4.Add(btnRemove, 0, RIGHT, 10)
        szr4.Add(btnOk, 0, RIGHT, 10)
        szr4.Add(btnCancel, 0)

        # szr5 :
        #        szr1
        #        szr2
        #        szr3
        #        szr4
        szr5 = BoxSizer(VERTICAL)
        szr5.Add(szr1, 0, GROW | ALL, 10)
        szr5.Add(szr2, 0, GROW | ALL, 10)
        szr5.Add(szr3, 0, GROW | ALL, 10)
        szr5.Add(szr4, 0, ALIGN_RIGHT | ALL, 10)

        self.SetSizer(szr5)
        self.SetAutoLayout(True)

        szr5.Fit(self)

    def updateLblArrow(self):
        """
        Draw an example arrow in lblArrow

        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        dic = {PyutLink: "Pyut Link"}
        self.logger.info(f"DlgEditLink-updateLblArrow: {self._pyutLink.__class__}")
        if self._pyutLink.__class__ in dic.keys():
            self._lblArrow.SetLabel(dic[self._pyutLink.__class__])
        else:
            # self._lblArrow.SetLabel("Unknown link class : " + self._pyutLink.__class__)
            self._lblArrow.SetLabel(f'Unknown link class : {self._pyutLink.__class__}')

    def _copyLink(self):
        """
        Copy the datas from _pyutLink to _pyutLinkCopy.

        @since 1.4
        @author P. Waelti <pwaelti@eivd.ch>
        """
        self._pyutLinkCopy = deepcopy(self._pyutLink)

    def _onTxtCardinalityAChange(self, event):
        """
        Event occurring when TXT_CARDINALITY_A change

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._cardinalityA = event.GetString()

    def _onTxtCardinalityBChange(self, event):
        """
        Event occurring when TXT_CARDINALITY_B change
        """
        self._cardinalityB = event.GetString()

    def _onTxtRelationshipChange(self, event):
        """
        Event occurring when TXT_RELATIONSHIP change
        """
        self._relationship = event.GetString()

    def _onTxtARoleBChange(self, event):
        """
        Event occurring when TXT_A_ROLE_IN_B change
        """
        self._aRoleInB = event.GetString()

    def _onTxtBRoleAChange(self, event):
        """
        Event occurring when TXT_B_ROLE_IN_A change
        """
        self._bRoleInA = event.GetString()

    # noinspection PyUnusedLocal
    def _onCmdOk(self, event: CommandEvent):
        """
        Handle click on "Ok" button

        Args:
            event:
        """
        self._pyutLink.name = self._relationship

        self._pyutLink.sourceCardinality      = self._cardinalityA
        self._pyutLink.destinationCardinality = self._cardinalityB
        # Should perhaps take roles, not yet implemented in PyutLink TODO

        self._returnAction = OK
        self.Close()

    # noinspection PyUnusedLocal
    def _onCmdCancel(self, event):
        """
        Handle click on "Cancel" button

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._returnAction = CANCEL
        self.Close()

    # noinspection PyUnusedLocal
    def _onRemove(self, event):
        """
        Handle click on "Remove" button

        @since 1.2
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._returnAction = -1
        self.Close()

    def getCardinality(self):
        """
        return a tuple composed by the two Cardinality (CA, CB)

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        return self._cardinalityA, self._cardinalityB

    def getRoles(self):
        """
        return a tuple composed by the two Roles (A's role in B, B's role in a)

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        return self._aRoleInB, self._bRoleInA

    def getRelationship(self):
        """
        return the relationship

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        return self._relationship

    def setValues(self, relationship, aRoleInB, bRoleInA, cardinalityA, cardinalityB):
        """
        set all link's values

        @param text relationship : the relationship between the two entities
        @param text aRoleInB     : the role of source entity in target entity
        @param text bRoleInA     : the role of target entity in source entity
        @param text cardinalityA : the source cardinality
        @param text cardinalityB : the target cardinality
        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._txtRelationship.SetValue(relationship)
        self._txtARoleB.SetValue(aRoleInB)
        self._txtBRoleA.SetValue(bRoleInA)
        self._txtCardinalityA.SetValue(cardinalityA)
        self._txtCardinalityB.SetValue(cardinalityB)

    def getReturnAction(self):
        """
        Return an info on how the user exited the dialog box

        @return : Ok = click on Ok button; Cancel = click on Cancel button
        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        return self._returnAction
