
from typing import cast

from org.pyut.history.HistoryUtils import COMMAND_CLASS_ID
from org.pyut.history.HistoryUtils import COMMAND_MODULE_ID
from org.pyut.history.HistoryUtils import makeValuatedToken


class Command:
    """

    This class is a part of the PyUt history capability.
    Every action that needs to be redone/undone should have an associated
    command. This class is to be considered an abstract class.
    """

    def __init__(self):
        """
        Notes:  Each Command should have at least one constructor with the
        same profile (no params), because it is this constructor that will
        be called when the history manager does deserialization.
        """
        from org.pyut.commands.CommandGroup import CommandGroup     # Avoid cyclical dependency

        self._group: CommandGroup = cast(CommandGroup, None)    # group to which the command is added. Init when added to a group

    def serialize(self) -> str:
        """

        Serialize the module name and class name;  All command must call
        this method in their implementation

        Notes:  Use `makeValuatedToken()` from HistoryUtils for each value
        you want to serialize

        Then you can use the `getTokenValue()` to get
        back the string representation of this value for the deserialization.

        Returns:  String representation of the command in view to store it
                  in a file. This method must be full implemented in all
                  subclasses.

                `return Command.serialize + (MyCommand's serialized information)`
        """
        moduleId: str = makeValuatedToken(COMMAND_MODULE_ID, str(self.__module__))
        classId:  str = makeValuatedToken(COMMAND_CLASS_ID, str(self.__class__.__name__))

        return f'{moduleId}{classId}'

    def deserialize(self, serializedInfo: str):
        """
        (Abstract) Here the developer should assign values to the information needed
        by the command (see also getTokenValue in historyUtils).

        Args:
            serializedInfo:

        Returns:    String from which we have to extract the information needed to
        set up the command.
        """
        pass

    def execute(self):
        """
        Do exactly the same as redo(), but is added for context clarity.
        It should be called instead of redo when we execute
        the command outside the history for the first time.

        It should be also called in the undo method of the contrary command

        e.g.

        createItem.undo() calls deleteItem.execute() and
        deleteItem.undo() calls createItem.execute()
        """
        self.redo()

    def redo(self):
        """
        (Abstract)Here should be implemented the code to redo the associated action
        """
        pass

    def undo(self):
        """
        This method should implement the code to undo the associated action. If
        there is a contrary command, use its execute() method.
        """
        pass

    def getGroup(self):
        """

        Returns:  The Command's CommandGroup
        """
        return self._group

    def setGroup(self, group):
        """
        Set the group to for the command. Avoid calling this method,
        because it is called automatically when the command is added to a group.

        Args:
            group:  group to which the command belongs.

        """
        self._group = group
