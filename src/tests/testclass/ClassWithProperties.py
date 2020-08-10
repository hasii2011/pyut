
from pyumldiagrams.Definitions import DiagramPadding


class ClassWithProperties:
    """
    Test both using .getter and .setter
    """

    def __init__(self):
        self._diagramPadding: DiagramPadding = DiagramPadding()

    @property
    def fontSize(self) -> int:
        """
        The font size to use in the generated UML diagram.  If unchanged the value is `pyumldiagrams.ClassWithProperties.ClassWithProperties.DEFAULT_FONT_SIZE`
        """
        return self._fontSize

    @fontSize.setter
    def fontSize(self, newSize: int):
        self._fontSize = newSize

    @property
    def verticalGap(self, newValue):
        self._diagramPadding.verticalGap = newValue

    @verticalGap.getter
    def verticalGap(self) -> int:
        return self._diagramPadding.verticalGap
