
from dataclasses import dataclass


@dataclass
class DTDAttribute:

    __slots__ = ['elementName', 'attributeName', 'attributeType', 'attributeValue', 'valueType']

    def __init__(self):
        pass

    elementName:    str
    attributeName:  str
    attributeType:  str
    attributeValue: str
    valueType:      int

