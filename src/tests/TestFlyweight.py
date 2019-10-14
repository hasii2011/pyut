
import unittest

from FlyweightString import FlyweightString
from org.pyut.PyutType import PyutType   # PyutType is a FlyweightString


class TestFlyweight(unittest.TestCase):
    """
    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def setUp(self):
        self.strings = [
            "salut", "hello", "ca va ?"
        ]

    def testFlyweightString(self):
        """Test whether instantiating an existing fly works correctly"""
        flies = []
        for string in self.strings:
            flies.append(FlyweightString(string))
        newFlies = []
        for string in self.strings:
            newFlies.append(FlyweightString(string))
        for oldFly, newFly in zip(flies, newFlies):
            self.assertTrue(newFly is oldFly, "duplicates in flies")

        # now, try with different strings with the same values
        a = FlyweightString("salut")
        b = FlyweightString("sa" + "lut")
        self.assertTrue(a is b, "two different objects with same values strings")

    def testPyutType(self):
        """Test PyutType class"""
        a: PyutType = PyutType("salut")
        b: PyutType = PyutType("s" + "alut")
        self.assertTrue(a.getName() == b.getName())
        self.assertTrue(a is b, "two different objects with same values strings")
        try:
            # noinspection PyUnresolvedReferences
            a.setName("Salut")
        except AttributeError:
            pass    # We should get this error
        else:
            self.fail("PyutType should not be modifiable by setName")


if __name__ == '__main__':
    unittest.main()
