
from typing import List

from pyutmodelv2 import PyutModelTypes

from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutClassCommon import PyutClassCommon
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.PyutLinkedObject import PyutLinkedObject
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutModifier import PyutModifier
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutObject import PyutObject
from pyutmodelv2.PyutParameter import PyutParameter
from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutSDMessage import PyutSDMessage
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutType import PyutType
from pyutmodelv2.PyutUseCase import PyutUseCase

from pyutmodelv2.enumerations.PyutDisplayParameters import PyutDisplayParameters
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType
from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype

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
    PyutModelTypes.__name__,
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
    PyutVisibility.__name__,
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
