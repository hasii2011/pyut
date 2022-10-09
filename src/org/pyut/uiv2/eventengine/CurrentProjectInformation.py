
from dataclasses import dataclass


@dataclass
class CurrentProjectInformation:
    """
    Typical use is by code that wants to update the application title
    """
    projectName:      str  = ''
    frameZoom:       float = 1.0
    projectModified: bool  = False
