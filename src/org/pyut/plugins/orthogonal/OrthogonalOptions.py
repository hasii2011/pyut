from dataclasses import dataclass

from org.pyut.plugins.orthogonal.OrthogonalOrientation import OrthogonalOrientation


@dataclass
class OrthogonalOptions:

    orientation:   OrthogonalOrientation = OrthogonalOrientation.VERTICAL
    layerSpacing:  float = 20.0
    nodeSpacing:   float = 75.0
    compactLayout: bool = False
