
from typing import List

from pyutmodel.ModelTypes import PyutLinks

from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutObject import PyutObject


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

        self._links:    PyutLinks              = PyutLinks([])
        self._parents:  List[PyutLinkedObject] = []     # Allows for multiple inheritance

    def getLinks(self) -> PyutLinks:
        """
        This is not a copy, but the original one. Any change made to it is
        directly made on the class.

        Returns: a list of the links.
        """
        return self._links

    def setLinks(self, links: PyutLinks):
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

    def __getstate__(self):
        """
        For deepcopy operations, tells which fields to avoid copying.
        Deepcopy must not copy the links to other classes, or it would result
        in copying all the diagram.
        """
        stateDict = self.__dict__.copy()
        stateDict["_links"] = []
        return stateDict
