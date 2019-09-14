#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from historyUtils import *
from delOglObjectCommand import *
from OglLinkFactory import *


class DelOglLinkCommand(DelOglObjectCommand):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    Every action that needs to be redone/undone should have an associated
    command. This class is to be considered as an abstract class.
    """
    
    def __init__(self, link = None):

        DelOglObjectCommand.__init__(self, link)

        self._srcPosition = None
        self._destPosition = None
        self._linkType = None
        self._linkSrcId = None
        self._linkDestId = None
        self._linkId = None

    #>------------------------------------------------------------------------
       
    def serialize(self):

        serialLink = Command.serialize(self)

        self._srcPosition = self._shape.GetSource().GetModel().GetPosition()
        self._destPosition = self._shape.GetDestination().GetModel().GetPosition()
        self._linkType = getLinkType(self._shape)
        self._linkSrcId = self._shape.getSourceShape().getPyutObject().getId()
        self._linkDestId = self._shape.getDestinationShape().getPyutObject().getId()
        self._linkId = self._shape.getPyutObject().getId()
        
        serialLink += makeValuatedToken("srcPosition", repr(self._srcPosition))
        serialLink += makeValuatedToken("destPosition", repr(self._destPosition))
        serialLink += makeValuatedToken("linkType", repr(self._linkType))
        serialLink += makeValuatedToken("linkSrcId", repr(self._linkSrcId))
        serialLink += makeValuatedToken("linkDestId", repr(self._linkDestId))
        serialLink += makeValuatedToken("linkId", repr(self._linkId))

        return serialLink
        
    #>------------------------------------------------------------------------
    
    def unserialize(self, serializedInfos):

        umlFrame = self.getGroup().getHistory().getFrame()
        
        self._srcPosition = eval(getTokenValue("srcPosition", serializedInfos))
        self._destPosition = eval(getTokenValue("destPosition", serializedInfos))
        self._linkType = eval(getTokenValue("linkType", serializedInfos))
        self._linkSrcId = eval(getTokenValue("linkSrcId", serializedInfos))
        self._linkDestId = eval(getTokenValue("linkDestId", serializedInfos))
        self._linkId = eval(getTokenValue("linkId", serializedInfos))

        self._shape = umlFrame.getUmlObjectById(self._linkId)

    #>------------------------------------------------------------------------

    def undo(self):

        umlFrame = self.getGroup().getHistory().getFrame()
        src = umlFrame.getUmlObjectById(self._linkSrcId)
        dest = umlFrame.getUmlObjectById(self._linkDestId)

        if self._shape is None :
            self._shape = umlFrame.createNewLink(src, dest, self._linkType)

        self._shape.getPyutObject().setId(self._linkId)
        self._shape.GetSource().GetModel().SetPosition(self._srcPosition[0], self._srcPosition[1])
        self._shape.GetDestination().GetModel().SetPosition(self._destPosition[0], self._destPosition[1] )
        self._shape.GetSource().UpdateFromModel()
        self._shape.GetDestination().UpdateFromModel()
        umlFrame.Refresh()
        
    #>------------------------------------------------------------------------
