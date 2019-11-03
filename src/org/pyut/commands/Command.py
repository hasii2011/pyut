
from org.pyut.history.HistoryUtils import COMMAND_CLASS_ID
from org.pyut.history.HistoryUtils import COMMAND_MODULE_ID
from org.pyut.history.HistoryUtils import makeValuatedToken


class Command:
    """
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (15.11.2005)
    This class is a part of the history system of PyUt.
    Every action that needs to be redone/undone should have an associated
    command. This class is to be considered as an abstract class.
    """

    def __init__(self):
        """
        Constructor.
        Notes : each Command should have at least one constructor with the
        same profile (no params), because it's this constructor that will
        be called when the history manager will do deserialization.
        """
        # group to which the command is added. Init when added to a group
        self._group = None

    def serialize(self):
        """
        return the module name and class name in view to read them during
        the unserialization and get the right constructor.

        @return a string representation of the command in view to store it
        in a file. This method must be redifined in all subclasses in that
        way :
            return Command.serialize + (MyCommand's serialized informations)

        Notes : use makeValuatedToken() from historyUtils for each value
        you want to serialize, so that you can use the getTokenValue to get
        back the string representation of this value for the unserialization.
        """

        return (makeValuatedToken(COMMAND_MODULE_ID, str(self.__module__)) +
                makeValuatedToken(COMMAND_CLASS_ID, str(self.__class__.__name__)))

    def deserialize(self, serializedInfo: str):
        """
        (Abstract) Here the developer should assign values to the information needed
        by the command (see also getTokenValue in historyUtils).
        @serializedInfo String :   string from which whe have to extract the informations needed to set up the command.
        """
        pass

    def execute(self):
        """
        Do exactly the same as redo(), but is added for context clearness.
        It should be called instead of redo when we execute for the first time
        the command outside the history. It should be also called in the undo
        method of the contrary command (for e.g. : createItem.undo() calls
        deleteItem.execute() and deleteItem.undo() calls createItem.execute())
        """
        self.redo()

    def redo(self):
        """
        (Abstract)Here should be implemented the code to redo the associated
        action
        """
        pass

    def undo(self):
        """
        here should be implemented the code to undo the associated action. If
        there is a contrary command, use its execute() method.
        """
        pass

    def getGroup(self):
        """
        @return the group (CommandGroup) to which belongs the command
        """
        return self._group

    def setGroup(self, group):
        """
        Set the group to which belongs the command. Avoid to call this method,
        because it is called automaticaly when the command is added to a group.
        @param group : group to which the command belongs.
        """
        self._group = group
