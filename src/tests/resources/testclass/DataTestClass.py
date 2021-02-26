from dataclasses import dataclass


@dataclass
class DataTestClass:

    z: int
    """
    property and type
    """
    w = "A string"
    """
    property and assignment
    """
    x: float = 0.0
    """
    full property, type and assignment
    """
    y: float = 42.0
    """
    full property, type and assignment
    """
