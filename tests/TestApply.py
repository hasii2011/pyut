
from unittest import TestCase
from unittest import TestSuite
from unittest import main as unitTestMain


from pyut.general.Globals import apply


def func(foo=None, bar=None):
    return foo, bar


class TestApply(TestCase):
    """
    Move this to hasiihelper
    Stolen from:  https://github.com/stefanholek/apply
    """

    def testNoargs(self):
        noargs = apply(func)
        self.assertEqual(noargs, (None, None), "None, None tuple was not returned")

    def testArgs(self):
        args = apply(func, args=(1,))
        self.assertEqual(args, (1, None), 'Did not get a tuple with a value')

    def testKeywordArguments(self):
        keywordArguments = apply(func, kwargs={'bar': 2})
        self.assertEqual(keywordArguments, (None, 2), 'Something wrong with keyword arguments')

    def testBasicApply(self):
        complexApply = apply(func, (1,), {'bar': 2})
        self.assertEqual(complexApply, (1, 2), 'Passing both types failed')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestApply))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
