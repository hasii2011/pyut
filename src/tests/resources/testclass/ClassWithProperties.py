# type: ignore

class ClassWithProperties:
    """
    Test both using .getter and .setter
    """

    def __init__(self,):
        self._fontSize:    int = 0
        self._verticalGap: int = 0

    @property
    def fontSize(self) -> int:
        return self._fontSize

    @fontSize.setter
    def fontSize(self, newSize: int):
        self._fontSize = newSize

    @property
    def verticalGap(self, newValue):
        self._verticalGap = newValue

    @verticalGap.getter
    def verticalGap(self) -> int:
        return self._verticalGap
