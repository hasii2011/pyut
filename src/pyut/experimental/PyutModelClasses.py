
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
from pyut.general.Singleton import Singleton

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
    "DisplayMethodParameters",
    "PyutActor",
    "PyutClass",
    "PyutClassCommon",
    "PyutDisplayParameters",
    "PyutField",
    "PyutInterface",
    "PyutLink",
    "PyutLinkedObject",
    "PyutLinkType",
    "PyutMethod",
    "PyutModifier",
    "PyutNote",
    "PyutObject",
    "PyutParameter",
    "PyutSDInstance"
    "PyutSDMessage",
    "PyutStereotype",
    "PyutText",
    "PyutType",
    "PyutUseCase",
    "PyutVisibilityEnum",
]

OglClassNames: List[str] = [
    "OglActor",
    "OglAggregation",
    "OglAssociation",
    "OglClass",
    "OglComposition",
    "OglInheritance",
    "OglInterface",
    "OglInterface2",
    "OglLink",
    "OglNote",
    "OglNoteLink",
    "OglObject",
    "OglText"
    "OglUseCase",
    "OglSDInstance",
    "OglSDMessage"
]
