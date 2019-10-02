#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from HistoryUtils1 import *
from command import *

class PrintCommand(Command):
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This is a command created only for testing pyut's history
    (see UnitTestHistory). The undo and redo method just print
    'undo' or 'redo' plus a user defined message.
    """

    def __init__(self):
        """
        Constructor.
        Notes: its profile matches with Command's one, so
        it can be called by the history (see Command)
        """

        Command.__init__(self)
        self._message = None

    #>-----------------------------------------------------------------------

    def setMessage(self, message):
        """
        set the message that will be displayed when we call undo/redo methods
        @param message (string)
        """
        self._message = message

    #>-----------------------------------------------------------------------

    def redo(self):

        print "redo : " + self._message

    #>-----------------------------------------------------------------------

    def undo(self):

        print "undo : " + self._message

    #>-----------------------------------------------------------------------

    def serialize(self):
        """
        serialize the message to display. DON't forget to call the serialize
        method of command.
        """

        return (Command.serialize(self) +
                makeValuatedToken("message", self._message))

    #>-----------------------------------------------------------------------

    def unserialize(self, serialCommand):
        """
        get from the serialized command the message to display
        and init the corresponding attribute.
        @param serialCommand (string)   :   serialized command
        """

        self._message = getTokenValue("message", serialCommand)
