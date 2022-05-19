
from typing import List

# These unused imports add in the classes so that the test code in UmlFrame.addHierarchy can do an introspection
# noinspection PyUnresolvedReferences
from pyutmodel.PyutClass import PyutClass
# noinspection PyUnresolvedReferences
from pyutmodel.PyutField import PyutField
# noinspection PyUnresolvedReferences
from pyutmodel.PyutLink import PyutLink
# noinspection PyUnresolvedReferences
from pyutmodel.PyutLinkedObject import PyutLinkedObject
# noinspection PyUnresolvedReferences
from pyutmodel.PyutNote import PyutNote
# noinspection PyUnresolvedReferences
from pyutmodel.PyutUseCase import PyutUseCase
# noinspection PyUnresolvedReferences
from pyutmodel.PyutActor import PyutActor
# noinspection PyUnresolvedReferences
from pyutmodel.PyutMethod import PyutMethod
# noinspection PyUnresolvedReferences
from pyutmodel.PyutModifier import PyutModifier
# noinspection PyUnresolvedReferences
from pyutmodel.PyutObject import PyutObject
# noinspection PyUnresolvedReferences
from pyutmodel.PyutParameter import PyutParameter
# noinspection PyUnresolvedReferences
from pyutmodel.PyutStereotype import PyutStereotype
# noinspection PyUnresolvedReferences
from pyutmodel.PyutType import PyutType
# noinspection PyUnresolvedReferences
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum
# noinspection PyUnresolvedReferences
from org.pyut.ui.Mediator import Mediator
# noinspection PyUnresolvedReferences
from org.pyut.general.Singleton import Singleton

# noinspection PyUnresolvedReferences
from ogl.OglObject import OglObject
# noinspection PyUnresolvedReferences
from ogl import OglClass
# noinspection PyUnresolvedReferences
from ogl import OglNote
# noinspection PyUnresolvedReferences
from ogl.OglActor import OglActor
# noinspection PyUnresolvedReferences
from ogl.OglUseCase import OglUseCase

# noinspection PyUnresolvedReferences
from ogl.OglLink import OglLink
# noinspection PyUnresolvedReferences
from ogl import OglNoteLink
# noinspection PyUnresolvedReferences
from ogl.OglAssociation import OglAssociation
# noinspection PyUnresolvedReferences
from ogl import OglAggregation
# noinspection PyUnresolvedReferences
from ogl.OglComposition import OglComposition
# noinspection PyUnresolvedReferences
from ogl.OglInheritance import OglInheritance
# noinspection PyUnresolvedReferences
from ogl.OglInterface import OglInterface
# noinspection PyUnresolvedReferences
from ogl.sd.OglSDInstance import OglSDInstance
# noinspection PyUnresolvedReferences
from ogl import OglLinkFactory

PyutClassNames: List[str] = [
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

OglClassNames: List[str] = [
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
