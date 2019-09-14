#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.9 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-1-8"

#from wxPython.wx import *
from pyutUtils import *
from PyutLink import *
from copy import deepcopy
import wx

[
    TXT_CARDINALITY_A, TXT_CARDINALITY_B, TXT_RELATIONSHIP,
    A_ROLE_IN_B, B_ROLE_IN_A, BTN_REMOVE
] = assignID(6)

class DlgEditLink (wx.Dialog):
    """
    Dialog for the link (between classes) edition.

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

    #>------------------------------------------------------------------------

    def __init__(self, parent, ID, pyutLink):
        """
        Constructor.

        @since 1.0
        @author C.Dutoit<dutoitc@hotmail.com>
        """

        wx.Dialog.__init__(self, parent, ID, _("Link Edit"),
                          style = wx.RESIZE_BORDER|wx.CAPTION)

        # Associated PyutLink
        self._pyutLink = pyutLink
        #~ self.SetSize(wx.Size(416, 200))

        #init members vars
        self._relationship = self._pyutLink.getName()
        self._aRoleInB = ""
        self._bRoleInA = ""
        self._cardinalityA = self._pyutLink.getSrcCard()
        self._cardinalityB = self._pyutLink.getDestCard()
        self._returnAction = wx.CANCEL#-1 #describe how user exited dialog box

        #labels
        lblCardA = wx.StaticText(self, -1, _("Cardinality"),
            style = wx.ALIGN_LEFT)
        lblRela  = wx.StaticText(self, -1, _("Relationship"),
            style = wx.ALIGN_CENTRE)
        lblCardB = wx.StaticText(self, -1, _("Cardinality"),
            style = wx.ALIGN_RIGHT)
        lblA     = wx.StaticText(self, -1, "A",      style = wx.ALIGN_LEFT)
        self._lblArrow = wx.StaticText(self, -1, "", style = wx.ALIGN_CENTRE)
        self.updateLblArrow()
        lblB     = wx.StaticText(self, -1, "B",      style = wx.ALIGN_RIGHT)
        lblAinB  = wx.StaticText(self, -1, _("A's role in B"),
            style = wx.ALIGN_LEFT)
        lblBinA  = wx.StaticText(self, -1, _("B's role in A"),
            style = wx.ALIGN_RIGHT)

        #text
        self._txtCardinalityA = wx.TextCtrl(self, TXT_CARDINALITY_A, "", 
               size = wx.Size(50, 20))
        self._txtRelationship = wx.TextCtrl(self, TXT_RELATIONSHIP,  "", 
               size = wx.Size(100, 20))
        self._txtCardinalityB = wx.TextCtrl(self, TXT_CARDINALITY_B, "", 
               size = wx.Size(50, 20))
        self._txtARoleB = wx.TextCtrl(self, A_ROLE_IN_B, "")
        self._txtBRoleA = wx.TextCtrl(self, B_ROLE_IN_A, "")

        #set old values (pwaelti)
        self.setValues(self._relationship, self._aRoleInB, self._bRoleInA, \
                       self._cardinalityA, self._cardinalityB)

        #disable roles (pwaelti)
        self._txtARoleB.Enable(False)
        self._txtBRoleA.Enable(False)

        #text events
        self.Bind(wx.EVT_TEXT, self._onTxtCardinalityAChange,id=TXT_CARDINALITY_A)
        self.Bind(wx.EVT_TEXT, self._onTxtCardinalityBChange,id=TXT_CARDINALITY_B)
        self.Bind(wx.EVT_TEXT, self._onTxtRelationshipChange,id=TXT_RELATIONSHIP)
        self.Bind(wx.EVT_TEXT, self._onTxtARoleBChange, id=A_ROLE_IN_B)
        self.Bind(wx.EVT_TEXT, self._onTxtBRoleAChange, id=B_ROLE_IN_A)

        #Ok/Cancel
        btnOk     = wx.Button(self, wx.OK, _("&Ok"))
        btnCancel = wx.Button(self, wx.CANCEL, _("&Cancel"))
        btnRemove = wx.Button(self, BTN_REMOVE, _("&Remove"))
        btnOk.SetDefault()

        #button events
        self.Bind(wx.EVT_BUTTON, self._onCmdOk, id=wx.OK)
        self.Bind(wx.EVT_BUTTON, self._onCmdCancel, id=wx.CANCEL)
        self.Bind(wx.EVT_BUTTON, self._onRemove, id=BTN_REMOVE)

        #dialog events
        #~ EVT_PAINT(self, self._onPaint)

        # Sizers (ndubois)
        
        # szr1 :
        # lblCardA,              lblRela,               lblCardB
        # self._txtCardinalityA, self._txtRelationship, self._txtCardinalityB
        szr1 = wx.FlexGridSizer(cols = 3, hgap = 30, vgap = 5)
        szr1.AddMany([
            (lblCardA, 0, wx.ALIGN_LEFT),
            (lblRela,  0, wx.ALIGN_CENTER_HORIZONTAL),
            (lblCardB, 0, wx.ALIGN_RIGHT),
            (self._txtCardinalityA, 0, wx.ALIGN_LEFT),
            (self._txtRelationship, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (self._txtCardinalityB, 0, wx.ALIGN_RIGHT)])
        szr1.AddGrowableCol(0)
        szr1.AddGrowableCol(1)
        szr1.AddGrowableCol(2)

        # szr2 :
        #        lblA, lblArrow, lblB
        szr2 = wx.BoxSizer(wx.HORIZONTAL)
        szr2.Add(lblA, 1, wx.GROW|wx.RIGHT, 10)
        szr2.Add(self._lblArrow, 1, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.RIGHT, 10)
        szr2.Add(lblB, 1, wx.GROW|wx.ALIGN_RIGHT)
        
        # szr3 :
        #        lblAinB,         lblBinA
        #        self._txtARoleB, self._txtBRoleA
        szr3 = wx.FlexGridSizer(cols = 2, hgap = 30, vgap = 5)
        szr3.AddMany([
            (lblAinB, 0),
            (lblBinA, 0, wx.ALIGN_RIGHT),
            (self._txtARoleB, 0),
            (self._txtBRoleA, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 20)])
        szr3.AddGrowableCol(0)
        szr3.AddGrowableCol(1)
        
        # szr4 :
        #        btnRemove, btnOk, btnCancel
        szr4 = wx.BoxSizer(wx.HORIZONTAL)
        szr4.Add(btnRemove, 0, wx.RIGHT, 10)
        szr4.Add(btnOk, 0, wx.RIGHT, 10)
        szr4.Add(btnCancel, 0)
        
        # szr5 :
        #        szr1
        #        szr2
        #        szr3
        #        szr4
        szr5 = wx.BoxSizer(wx.VERTICAL)
        szr5.Add(szr1, 0, wx.GROW|wx.ALL, 10)
        szr5.Add(szr2, 0, wx.GROW|wx.ALL, 10)
        szr5.Add(szr3, 0, wx.GROW|wx.ALL, 10)
        szr5.Add(szr4, 0, wx.ALIGN_RIGHT|wx.ALL, 10)

        self.SetSizer(szr5)
        self.SetAutoLayout(True)

        szr5.Fit(self)

    #>------------------------------------------------------------------------

    def updateLblArrow(self):
        """
        Draw an example arrow in lblArrow

        @since 1.1.1.2
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        #if self._pyutLink.__class__=="PyutLink.PyutLink
        #print self._pyutLink.__class__
        #print dir(self._lblArrow)
        #print type(self._pyutLink)
        #self._pyutLink.SetLabel("Hello world")

        dic = {PyutLink : "Pyut Link"}
        print "DlgEditLink-updateLblArrow ", self._pyutLink.__class__
        if self._pyutLink.__class__ in dic.keys():
            self._lblArrow.SetLabel(dic[self._pyutLink.__class__])
        else:
            self._lblArrow.SetLabel("Unknown link class : " + \
                                    self._pyutLink.__class__)




    #>------------------------------------------------------------------------

    def _copyLink(self):
        """
        Copy the datas from _pyutLink to _pyutLinkCopy.

        @since 1.4
        @author P. Waelti <pwaelti@eivd.ch>
        """
        self._pyutLinkCopy = deepcopy(self._pyutLink)


    #>------------------------------------------------------------------------

    #~ def _onPaint(self, event):
        #~ """
        #~ Redraw the arrow

        #~ @since 1.2
        #~ @author C.Dutoit<dutoitc@hotmail.com>
        #~ """
        #~ #Draw the relation's arrow
        #~ dc=wx.PaintDC(self)
        #~ dc.BeginDrawing()
        #~ dc.DrawLine((24, 64), (376, 64))
        #~ dc.DrawLine((360, 56), (376, 64))
        #~ dc.DrawLine((360, 72), (376, 64))
        #~ dc.EndDrawing()

    #>------------------------------------------------------------------------

    def _onTxtCardinalityAChange(self, event):
        """
        Event occuring when TXT_CARDINALITY_A change

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._cardinalityA=event.GetString()

    #>------------------------------------------------------------------------

    def _onTxtCardinalityBChange(self, event):
        """
        Event occuring when TXT_CARDINALITY_B change

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._cardinalityB=event.GetString()

    #>------------------------------------------------------------------------

    def _onTxtRelationshipChange(self, event):
        """
        Event occuring when TXT_RELATIONSHIP change

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._relationship=event.GetString()

    #>------------------------------------------------------------------------

    def _onTxtARoleBChange(self, event):
        """
        Event occuring when TXT_A_ROLE_IN_B change

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._aRoleInB=event.GetString()

    #>------------------------------------------------------------------------

    def _onTxtBRoleAChange(self, event):
        """
        Event occuring when TXT_B_ROLE_IN_A change

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._bRoleInA=event.GetString()

    #>------------------------------------------------------------------------

    def _onCmdOk(self, event):
        """
        Handle click on "Ok" button

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """

        self._pyutLink.setName(self._relationship)
        self._pyutLink.setSrcCard(self._cardinalityA)
        self._pyutLink.setDestCard(self._cardinalityB)

        # Should perhaps take roles, not yet implemented in PyutLink TODO

        self._returnAction=wx.OK
        self.Close()


    #>------------------------------------------------------------------------

    def _onCmdCancel(self, event):
        """
        Handle click on "Cancel" button

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        self._returnAction=wx.CANCEL
        self.Close()

    #>------------------------------------------------------------------------

    def _onRemove(self, event):
        """
        Handle click on "Remove" button

        @since 1.2
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._returnAction = -1
        self.Close()

    #>------------------------------------------------------------------------

    def getCardinality(self):
        """
        return a tuple composed by the two Cardinality (CA, CB)

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        return (self._cardinalityA, self._cardinalityB)

    #>------------------------------------------------------------------------

    def getRoles(self):
        """
        return a tuple composed by the two Roles (A's role in B, B's role in a)

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        return (self._aRoleInB, self._bRoleInA)

    #>------------------------------------------------------------------------

    def getRelationship(self):
        """
        return the relationship

        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        return self._relationship

    #>------------------------------------------------------------------------

    def setValues(self, relationship, aRoleInB, bRoleInA, 
                  cardinalityA, cardinalityB):
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

    #>------------------------------------------------------------------------

    def getReturnAction(self):
        """
        Return an info on how the user exited the dialog box

        @return : wx.Ok = click on Ok button; wx.Cancel = click on Cancel button
        @since 1.2
        @author C.Dutoit<dutoitc@hotmail.com>
        """
        return self._returnAction
