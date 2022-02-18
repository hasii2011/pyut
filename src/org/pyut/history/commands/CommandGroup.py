
from typing import List

from logging import Logger
from logging import getLogger

from importlib import import_module

from org.pyut.history.commands.Command import Command

from org.pyut.history.HistoryUtils import COMMAND_BEGIN_ID
from org.pyut.history.HistoryUtils import COMMAND_CLASS_ID
from org.pyut.history.HistoryUtils import COMMAND_END_ID
from org.pyut.history.HistoryUtils import COMMAND_MODULE_ID
from org.pyut.history.HistoryUtils import GROUP_BEGIN_ID
from org.pyut.history.HistoryUtils import GROUP_COMMENT_ID
from org.pyut.history.HistoryUtils import GROUP_END_ID
from org.pyut.history.HistoryUtils import TOKEN_BEGIN
from org.pyut.history.HistoryUtils import TOKEN_END

from org.pyut.history.HistoryUtils import deTokenize
from org.pyut.history.HistoryUtils import tokenize
from org.pyut.history.HistoryUtils import tokenizeValue


class CommandGroup:
    """


    This class is a part of the history system of PyUt. It brings together
    different commands used for doing undo or redo.
    For example, when we
    select many shapes, and we delete them, then there is a command 'created'
    for each one that is added to a CommandGroup. This way, when we want
    to undo, all the deleted shapes will be reconstructed in one action.
    """
    def __init__(self, comment=""):
        """

        Args:
            comment:  a short description/comment in view to display in the menu or other GUI part.
        """
        self.logger: Logger = getLogger(__name__)

        self._history = None
        """
        history to which belongs the group. Init when the group is added.
        """
        self._commands: List[Command] = []
        """
        list of commands belonging to the group
        """
        self._comment:    str = comment
        self._commonData: List = []
        """
        Stores information that is common to all the commands in the
        group. 
        WARNING : the common data is NOT serialized, so the
        common data is lost after a deserialization. You have to use
        this data in a command before the serialization.        
        """

    def addCommand(self, command: Command):
        """
        Add the specified command to the group
        Args:
            command:  The command to add
        """
        command.setGroup(self)
        self._commands.append(command)

    def removeCommand(self, command: Command):
        """
        Remove the specified command from the group
        @param command  : command to remove
        """

        self._commands.remove(command)

    def serialize(self):
        """
        Transform all the commands belonging to the group into strings in
        view to store them in a file.
        @return a string representing the command.
        """
        # add the beginning information of the group
        serializedGroup = (tokenize(GROUP_BEGIN_ID) + tokenizeValue(GROUP_COMMENT_ID, self._comment))
        # add the beginning information and setup information of
        # each command. After that add the ending information of
        # for each command.
        for command in self._commands:
            serializedGroup += (tokenize(COMMAND_BEGIN_ID) + command.serialize() + tokenize(COMMAND_END_ID))

        # add the ending information of the group
        serializedGroup += tokenize(GROUP_END_ID)

        return serializedGroup

    def deserialize(self, serializedCommands: str):
        """
        deserialize the specified commands and add them to the group

        Args:
            serializedCommands:   a string representation of the commands belonging to the group.
        """
        # define the beginning and ending token of a serialized command
        commandBegin = TOKEN_BEGIN + COMMAND_BEGIN_ID + TOKEN_END
        commandEnd   = TOKEN_BEGIN + COMMAND_END_ID + TOKEN_END

        # looking for the beginning of the first command
        cStart = serializedCommands.find(commandBegin)
        self.logger.info(f'cStart: {cStart}')
        # while there is still a command beginning token we can proceed to the deserialization.
        while cStart > -1:

            # we do not need any more of the beginning token
            cStart += len(commandBegin)
            self.logger.info(f'cStart - commandBegin: {cStart}')

            # find the ending token for this command
            cEnd = serializedCommands.find(commandEnd, cStart)

            # we work only on the useful data
            serialCommand = serializedCommands[cStart: cEnd]

            commandModuleName = deTokenize(COMMAND_MODULE_ID, serialCommand)
            self.logger.info(f'commandModuleName: {commandModuleName}')

            # get the name of the class of the command
            commandClassName = deTokenize(COMMAND_CLASS_ID, serialCommand)
            self.logger.info(f'commandClassName: {commandClassName}')

            # import the module which contains the command class and get the class (cls)
            moduleName = import_module(commandModuleName)
            commandClass = getattr(moduleName, commandClassName)

            # construction of an uninitialized command
            try:
                command = commandClass()
                command.setGroup(self)

                # deserialization and setup of the command
                command.deserialize(serialCommand)

                # add the command to the group
                self.addCommand(command)

                # looking for the next command beginning token
                cStart = serializedCommands.find(commandBegin, cEnd)
                self.logger.info(f'cStart - serializedCommands: {cStart}')

            except (ValueError, Exception) as e:
                self.logger.error(f'Error during deserialization: {e}')

    def redo(self):
        """
        Call the redo() method of all commands belonging to the group
        """
        for command in self._commands:
            command.redo()

    def undo(self):
        """
        Call the `undo` method of all commands belonging to the group
        """
        for command in self._commands:
            command.undo()

    def execute(self):
        """
        Call the `execute` method of all commands belonging to the group
        """
        for command in self._commands:
            command.execute()

    def getHistory(self):
        """
        return the group history
        """
        return self._history

    def setHistory(self, history):
        """
        Set the history to which belongs the group. Avoid to calling method
        because it is called automatically when the group is added.

        @param history  : history to which belongs the group
        """

        self._history = history

    def getComment(self) -> str:
        """
        return the comment/description of the group
        """

        return self._comment

    def setComment(self, comment: str):
        """
        set the comment/description of the group

        Args:
            comment: comment/description of group to display
        """

        self._comment = comment

    def addCommonData(self, commonData: List):
        """
        Add a data that is common to all the commands belonging to this group.

        Common data should contain an identifier so that a given command
        can get only the pertinent data for itself. For e.g. linkCommand will
        get only the tuples ("link", (shapeToLink, linkId)).

        WARNING : the common data is NOT serialized, so it is lost after
        a deserialization. You have to use this data in a command before
        the serialization of the group.

        Args:
            commonData:   data list that a command adds to be used by another command.
        """
        self._commonData.append(commonData)

    def getCommonData(self) -> List:
        """
        WARNING : The common data is NOT serialized, so it is lost after
        a deserialization. You have to use these data in a command before
        the serialization of the group.

        Returns: A list of common data, so a command can use information
        produced by another command in the same group.

        """
        return self._commonData

    def __repr__(self):
        return f'Comment: `{self._comment}` Common Data: `{self._commonData}`'
