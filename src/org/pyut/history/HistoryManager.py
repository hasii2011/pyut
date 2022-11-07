
from typing import cast

from logging import Logger
from logging import getLogger

from os import sep as osSep

from tempfile import gettempdir

from pyut.preferences.PyutPreferences import PyutPreferences

from org.pyut.history.commands.CommandGroup import CommandGroup

from org.pyut.history.HistoryUtils import GROUP_COMMENT_ID
from org.pyut.history.HistoryUtils import HISTORY_FILE_NAME
from org.pyut.history.HistoryUtils import deTokenize

from pyut.PyutUtils import PyutUtils


class HistoryManager:
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)

    This class is the structure that manages the history of a given frame.
    It creates a file where serialized 'CommandGroups' are stored.  They
    are compound commands. Each command is able to do the undo/redo
    operations and is also able to serialize/deserialize itself
    (See commandGroup and command).

    To see how it works, please see `tests.org.pyut.history.TestHistoryManager`

    TODO: from Humberto.  It appears that `redo` can only redo things that have been undone (`undo`); I do not want it work to work this way
    """
    historyId = 0
    """
    defines a unique id that will be added to the file base name
    in order to have a unique file associated to each instance of
    the history.
    """
    def __init__(self, theFrame=None):
        """

        Args:
            theFrame:  The UML Frame to which this history is attached.
        """
        self.logger:    Logger = getLogger(__name__)

        self.logger.debug(f'Base directory: {PyutUtils.getBasePath()}')

        if PyutPreferences().useDebugTempFileLocation is True:
            self._fileName: str = f'{PyutUtils.getBasePath()}{osSep}{HISTORY_FILE_NAME}{str(self.__class__.historyId)}'
        else:
            tempDir: str = gettempdir()
            self._fileName: str = f'{tempDir}{osSep}{HISTORY_FILE_NAME}{str(self.__class__.historyId)}'

        self._frame    = theFrame
        """
        name of file for hard storage which is unique for each history
        """
        self.__class__.historyId += 1
        """
        for the next instance of the history...
        """
        saveFile = open(self._fileName, 'w')  # create the file to store the groups
        saveFile.close()

        self._groupCount = 0
        """
        number of groups added to the history
        """
        self._groupUndoIndex = -1
        """
        index of the command group that will be undone
        """
        self._groupToExecute: CommandGroup = cast(CommandGroup, None)
        """
        reference to the last added group, for execute() method
        """

    def getGroupCount(self) -> int:
        return self._groupCount

    def setGroupCount(self, newValue: int):
        raise NotImplementedError('Group count is read-only')

    def getGroupUndoIndex(self) -> int:
        return self._groupUndoIndex

    def setGroupUndoIndex(self, newValue: int = -1):
        raise NotImplementedError('Group undo index is read-only')

    def getGroupToExecute(self) -> CommandGroup:
        return self._groupToExecute

    def setGroupToExecute(self, newValue: CommandGroup):
        raise NotImplementedError('Group to execute is read-only')

    groupCount     = property(getGroupCount, setGroupCount)
    groupUndoIndex = property(getGroupUndoIndex, setGroupUndoIndex)
    groupToExecute = property(getGroupToExecute, setGroupToExecute)

    def undo(self):
        """
        undo the current group command and make the previous one as current.
        """

        # check if there is a group to undo
        if self.isUndoPossible():

            # open the file to get its current content in a list
            saveFile = open(self._fileName, 'r')
            fileContent = saveFile.readlines()
            saveFile.close()

            # deserialize the group to undo
            group = self._deserialize(fileContent[self._groupUndoIndex])
            group.setHistory(self)

            # undo all the commands that are in the group
            group.undo()

            # set the previous command as the command to be undone
            self._groupUndoIndex -= 1

    def redo(self):
        """
        take from the file the last undone command group and redo it.
        """
        # check if there is a group to redo
        if self.isRedoPossible():

            # open the file to get its current content in a list
            saveFile = open(self._fileName, 'r')
            fileContent = saveFile.readlines()
            saveFile.close()

            # the group to redo means that it will be the group to undo
            self._groupUndoIndex += 1

            # deserialize the group
            group = self._deserialize(fileContent[self._groupUndoIndex])
            group.setHistory(self)

            # redo all the commands in the group
            group.redo()

    def execute(self):
        """
        execute the last added command group and remove it after that.
        """

        self._groupToExecute.execute()
        self._groupToExecute = None

    def addCommandGroup(self, group: CommandGroup):
        """
        add a command group to the file.
        @param group   :   group to add to the history.
        """

        group.setHistory(self)

        self._groupToExecute = group

        # open the file to get its current content in a list
        saveFile = open(self._fileName, 'r')
        fileContent = saveFile.readlines()
        saveFile.close()

        # add the serialized group to the file's content
        serialGroup = self._serialize(group)
        self._groupUndoIndex += 1
        fileContent.insert(self._groupUndoIndex, serialGroup)

        # remove all the groups that comes after new group
        del fileContent[self._groupUndoIndex + 1: len(fileContent) + 1]

        # update the number of groups present in the history
        self._groupCount = len(fileContent)

        # save the new content on file, writing over the old content.
        saveFile = open(self._fileName, 'w')
        saveFile.writelines(fileContent)
        saveFile.close()

    def destroy(self):
        """
        Destroy the file associated to the history. Should be called when
        the associated frame is closing.
        """
        import os
        os.remove(self._fileName)

    def isUndoPossible(self):
        """
        Enables or disables the undo item in the application menuItem

        Returns: 'True' if undo is possible, else 'False'
        """
        # the first group added has the index 0...
        return self._groupUndoIndex > -1

    def isRedoPossible(self):
        """
        @return a boolean indicating if a redo is possible. Use it for e.g.
        (un)enable the redo item in a menu.
        """
        # groupToUndo index begins at 0 so the count is bigger of one if
        # groupToUndo is on the last group added. If it's the case, then
        # it means that the last group hadn't been undone and so there is
        # no group to redo.
        return self._groupUndoIndex < self._groupCount - 1

    def getCommandGroupToRedo(self):
        """
        @return the group (CommandGroup) that will be redone if we call
        the undo method. If all the groups have been undone None is returned.
        """
        # check if there is a group to redo
        if self.isRedoPossible():

            # open the file to get its current content in a list
            saveFile = open(self._fileName, 'r')
            fileContent = saveFile.readlines()
            saveFile.close()

            # get the group that is next to be redone
            group = self._deserialize(fileContent[self._groupUndoIndex + 1])
            group.setHistory(self)
            return group
        else:
            return None

    def getCommandGroupToUndo(self):
        """
        @return The group (CommandGroup) that will be redone if we call
        the undo method. If all the groups have been undone None is returned.
        """

        # check if there is a group to undo
        if self.isUndoPossible():

            # open the file to get its current content in a list
            saveFile = open(self._fileName, 'r')
            fileContent = saveFile.readlines()
            saveFile.close()

            # get the group that is next to be redone
            group = self._deserialize(fileContent[self._groupUndoIndex])
            group.setHistory(self)
            return group
        else:
            return None

    def getFrame(self):
        """
        @return the associated to the history frame
        """

        return self._frame

    def _deserialize(self, serializedGroup) -> CommandGroup:
        """
        deserialize the specified string to return a command group

        Args:
            serializedGroup: (string)  :   string from which will be constructed the group

        Returns:    an initialized group (CommandGroup)
        """
        # get from the string the comment/description for the group
        grpComment = deTokenize(GROUP_COMMENT_ID, serializedGroup)

        # create an initialized group with only its comment
        group = CommandGroup(grpComment)
        group.setHistory(self)

        # deserialize the commands belonging to the group
        group.deserialize(serializedGroup)

        return group

    def _serialize(self, group):
        """
        serialize a group to store it in a file. Each serialized group is on
        one line.
        """
        return group.serialize() + "\n"
