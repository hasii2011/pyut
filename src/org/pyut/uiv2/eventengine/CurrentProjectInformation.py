
from dataclasses import dataclass


@dataclass
class CurrentProjectInformation:
    projectName:      str  = ''
    frameZoom:       float = 1.0
    projectModified: bool  = False
