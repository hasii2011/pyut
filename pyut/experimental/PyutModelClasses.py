
from typing import List

from pyutmodel.PyutDisplayParameters import PyutDisplayParameters
from pyutmodel import ModelTypes
from pyutmodel.PyutActor import PyutActor
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutClassCommon import PyutClassCommon
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkedObject import PyutLinkedObject
from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutModifier import PyutModifier
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutObject import PyutObject
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutSDInstance import PyutSDInstance
from pyutmodel.PyutSDMessage import PyutSDMessage
from pyutmodel.PyutStereotype import PyutStereotype
from pyutmodel.PyutText import PyutText
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutUseCase import PyutUseCase
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from ogl.OglActor import OglActor
from ogl.OglAggregation import OglAggregation
from ogl.OglAssociation import OglAssociation
from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglClass import OglClass
from ogl.OglComposition import OglComposition
from ogl import OglConstants
from ogl.OglDimensions import OglDimensions
from ogl.OglInheritance import OglInheritance
from ogl.OglInterface import OglInterface
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglLinkFactory import OglLinkFactory
from ogl.OglNote import OglNote
from ogl.OglNoteLink import OglNoteLink
from ogl.OglObject import OglObject
from ogl.OglPosition import OglPosition
from ogl.OglText import OglText
from ogl.OglTextFontFamily import OglTextFontFamily
from ogl.OglUseCase import OglUseCase
from ogl.OglUtils import OglUtils

from ogl.sd.OglInstanceName import OglInstanceName
from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

PyutClassNames: List[str] = [
    ModelTypes.__name__,
    PyutActor.__name__,
    PyutClass.__name__,
    PyutClassCommon.__name__,
    PyutDisplayParameters.__name__,
    PyutField.__name__,
    PyutInterface.__name__,
    PyutLink.__name__,
    PyutLinkedObject.__name__,
    PyutLinkType.__name__,
    PyutMethod.__name__,
    PyutModifier.__name__,
    PyutNote.__name__,
    PyutObject.__name__,
    PyutParameter.__name__,
    PyutSDInstance.__name__,
    PyutSDMessage.__name__,
    PyutStereotype.__name__,
    PyutText.__name__,
    PyutType.__name__,
    PyutUseCase.__name__,
    PyutVisibilityEnum.__name__,
]

OglClassNames: List[str] = [
    OglActor.__name__,
    OglAggregation.__name__,
    OglAssociation.__name__,
    OglAssociationLabel.__name__,
    OglClass.__name__,
    OglComposition.__name__,
    OglConstants.__name__,
    OglDimensions.__name__,
    OglInheritance.__name__,
    OglInterface.__name__,
    OglInterface2.__name__,
    OglLink.__name__,
    OglLinkFactory.__name__,
    OglNote.__name__,
    OglNoteLink.__name__,
    OglObject.__name__,
    OglPosition.__name__,
    OglText.__name__,
    OglTextFontFamily.__name__,
    OglUseCase.__name__,
    OglUtils.__name__,
    OglInstanceName.__name__,
    OglSDInstance.__name__,
    OglSDMessage.__name__
]
