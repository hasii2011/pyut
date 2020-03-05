
from typing import List

from org.pyut.model.PyutLink import PyutLink
from org.pyut.model.PyutObject import PyutObject


class PyutLinkedObject(PyutObject):
    """
    An object which can be connected to other one.
    This class provides all support for link management in the data layer. All
    classes that may be interconnected (classes for examples) should inherit
    this class to have all links support.
    """
    def __init__(self, name=""):
        """

        Args:
            name:  The object name
        """
        super().__init__(name)

        self._links:    List[PyutLink]         = []
        self._parents:  List[PyutLinkedObject] = []     # Allows for multiple inheritance
        self._filename: str            = ""

    def computeNextSafeID(self):
        """
        Get the next safe id

        @author C.Dutoit
        """
        # Verify that next id is not already used
        while self.isIDUsed(PyutLinkedObject.nextId):
            PyutLinkedObject.nextId += 1

    def getLinks(self) -> List[PyutLink]:
        """
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        Returns: a list of the links.
        """
        return self._links

    def setLinks(self, links: List[PyutLink]):
        """
        Replace the actual links by those given in the list.
        The methods passed are not copied, but used directly.

        Args:
            links:
        """
        self._links = links

    def addLink(self, link: PyutLink):
        """
        Add the given link to the links

        Args:
            link:   The new link to add
        """
        self._links.append(link)

    def getParents(self) -> List["PyutLinkedObject"]:
        """
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        Returns:          Return a list of the parents.
        """
        return self._parents

    def setParents(self, parents: List["PyutLinkedObject"]):
        """
        Replace the actual parents by those given in the list.
        The methods passed are not copied, but used directly.

        Args:
            parents:
        """
        self._parents = parents

    def addParent(self, parent: "PyutLinkedObject"):
        """
        Add a parent to the parent list

        Args:
            parent:
        """
        self._parents.append(parent)

    def setFilename(self, filename: str):
        """
        Set the associated filename.
        This is used by the reverse engineering plugins.

        Args:
            filename:  the file name
        """
        self._filename = filename

    def getFilename(self) -> str:
        """
        Get the associated filename.

        Returns: An empty is returned if there is no filename.
        """
        return self._filename

    def __getstate__(self):
        """
        For deepcopy operations, tells which fields to avoid copying.
        Deepcopy must not copy the links to other classes, or it would result
        in copying all the diagram.
        """
        stateDict = self.__dict__.copy()
        stateDict["_links"] = []
        return stateDict
