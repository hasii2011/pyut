

class ClassWithMethodsWithDefaultValues:

    def __init__(self):
        self._value1: float = 0
        self._value2: float = 0
        self._value3: float = 0
        self._value4: float = 0

    def methodWithDefaultValues(self, param1, param2: float, param3=57.0, param4: float = 42.0):

        self._value1 = param1
        self._value2 = param2
        self._value3 = param3
        self._value4 = param4
