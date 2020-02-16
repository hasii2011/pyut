
from typing import List

# These unused imports add in the classes so that the test code in UmlFrame.addHierarchy can do an introspection
# noinspection PyUnresolvedReferences
from org.pyut.PyutClass import PyutClass
# noinspection PyUnresolvedReferences
from org.pyut.model.PyutField import PyutField
# noinspection PyUnresolvedReferences
from org.pyut.PyutLink import PyutLink
# noinspection PyUnresolvedReferences
from org.pyut.PyutLinkedObject import PyutLinkedObject
# noinspection PyUnresolvedReferences
from org.pyut.model.PyutNote import PyutNote
# noinspection PyUnresolvedReferences
from org.pyut.model.PyutUseCase import PyutUseCase
# noinspection PyUnresolvedReferences
from org.pyut.model.PyutActor import PyutActor
# noinspection PyUnresolvedReferences
from org.pyut.PyutMethod import PyutMethod
# noinspection PyUnresolvedReferences
from org.pyut.model.PyutModifier import PyutModifier
# noinspection PyUnresolvedReferences
from org.pyut.PyutObject import PyutObject
# noinspection PyUnresolvedReferences
from org.pyut.PyutParam import PyutParam
# noinspection PyUnresolvedReferences
from org.pyut.model.PyutStereotype import PyutStereotype
# noinspection PyUnresolvedReferences
from org.pyut.model.PyutType import PyutType
# noinspection PyUnresolvedReferences
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum
# noinspection PyUnresolvedReferences
from org.pyut.general.Mediator import Mediator
# noinspection PyUnresolvedReferences
from org.pyut.general.Singleton import Singleton

# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglObject import OglObject
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglClass import OglClass
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglNote import OglNote
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglActor import OglActor
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglUseCase import OglUseCase

# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglLink import OglLink
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglNoteLink import OglNoteLink
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglAssociation import OglAssociation
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglAggregation import OglAggregation
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglComposition import OglComposition
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglInheritance import OglInheritance
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglInterface import OglInterface
# noinspection PyUnresolvedReferences
from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
# noinspection PyUnresolvedReferences
from org.pyut.ogl.OglLinkFactory import OglLinkFactory

display: List[str] = [
    "PyutClass",
    "PyutField",
    "PyutLink",
    "PyutLinkedObject",
    "PyutNote",
    "PyutUseCase",
    "PyutActor",
    "PyutMethod",
    "PyutModifier",
    "PyutObject",
    "PyutParam",
    "PyutStereotype",
    "PyutType",
    "PyutVisibility",
    "PyutSDMessage",
    "Mediator",
    "Singleton",
]

displayOgl: List[str] = [
    "OglObject",
    "OglClass",
    "OglNote",
    "OglActor",
    "OglUseCase",
    "OglLink",
    "OglNoteLink",
    "OglAssociation",
    "OglAggregation",
    "OglComposition",
    "OglSDInstance",
    "OglInheritance",
    "OglInterface",
    "OglLinkFactory"
]
