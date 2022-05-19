
from enum import Enum


class OglEventType(Enum):
    """
    These should match the actual event definitions in OglEvents
    """

    ShapeSelected           = 'ShapeSelected'
    CutOglClass             = 'CutOglClass'
    ProjectModified         = 'ProjectModified'
    RequestLollipopLocation = 'RequestLollipopLocation'
    CreateLollipopInterface = 'CreateLollipopInterface'

