
from logging import Logger
from logging import getLogger

from unittest import TestSuite

from unittest import main as unitTestMain

from org.pyut.general.SemanticVersion import SemanticVersionError
from org.pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase


from org.pyut.general.SemanticVersion import SemanticVersion

GOOD_PREVIOUS_BASIC_VERSION: str = '6.1.0'
GOOD_BASIC_VERSION:          str = '6.2.1'

GOOD_BUILD_NUMBER:  str = f'{GOOD_BASIC_VERSION}+.5988'
GOOD_PRE_RELEASE:   str = '7.0.0-Alpha.1.1.1'


class TestSemanticVersion(TestBase):

    """
    """
    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestSemanticVersion.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

    def setUp(self):
        self.logger: Logger = TestSemanticVersion.clsLogger

    def tearDown(self):
        pass

    def testGoodStr(self):

        self.assertEqual(str(SemanticVersion('0.0.0')), '0.0.0')

    def testGoodPatchVersion(self):
        self.assertEqual(SemanticVersion(GOOD_BASIC_VERSION).patch, 1, 'Must Be true')

    def testGoodMinorVersion(self):
        self.assertEqual(SemanticVersion(GOOD_BASIC_VERSION).minor, 2, 'Must Be true')

    def testGoodMajorVersion(self):
        self.assertEqual(SemanticVersion(GOOD_BASIC_VERSION).major, 6, 'Must Be true')

    def testGoodBasicVersion(self):

        try:
            goodVersion: str = GOOD_BASIC_VERSION
            semanticVersion: SemanticVersion = SemanticVersion(goodVersion)
            self.assertIsNotNone(semanticVersion, 'Did not initialize')

            self.logger.info(f'Good Basic Version: {semanticVersion}')
        except SemanticVersionError as sve:
            self.fail(f'{sve}')

    def testGoodVersionWithBuildNumber(self):
        try:

            semanticVersion: SemanticVersion = SemanticVersion(GOOD_BUILD_NUMBER)
            self.assertIsNotNone(semanticVersion, 'Did not initialize')

            self.logger.info(f'Good Version with BuildNumber: {semanticVersion}')

        except SemanticVersionError as sve:
            self.fail(f'{sve}')

    def testGoodPreReleaseVersion(self):
        try:
            semanticVersion: SemanticVersion = SemanticVersion(GOOD_PRE_RELEASE)
            self.assertIsNotNone(semanticVersion, 'Did not initialize')

            self.logger.info(f'Good Pre-Release Version: {semanticVersion.__repr__()}')

        except SemanticVersionError as sve:
            self.fail(f'{sve}')

    def testBadVersion(self):

        try:
            badVersion: str = 'x.x.x'
            semanticVersion: SemanticVersion = SemanticVersion(badVersion)

            self.assertTrue(False, f'{semanticVersion} should have thrown exception')
        except SemanticVersionError as se:
            self.logger.info(f'Expected: {se}')

    def testMajorMinorPatchEqual(self):

        sv1: SemanticVersion = SemanticVersion(GOOD_BASIC_VERSION)
        sv2: SemanticVersion = SemanticVersion(GOOD_BASIC_VERSION)

        self.assertEqual(sv1, sv2, 'These should be the same semantic version')

    def testMajorMinorPatchNotEqual(self):

        sv1: SemanticVersion = SemanticVersion(GOOD_BASIC_VERSION)
        sv2: SemanticVersion = SemanticVersion('6.1.2')

        self.assertNotEqual(sv1, sv2, 'These should NOT be the same semantic version')

    def testMajorMinorPatchBuildNumberEqual(self):

        sv1: SemanticVersion = SemanticVersion(GOOD_BUILD_NUMBER)
        sv2: SemanticVersion = SemanticVersion(GOOD_BUILD_NUMBER)

        self.assertEqual(sv1, sv2, 'These should be the same semantic version with a build number')

    def testMajorMinorPatchBuildNumberNotEqual(self):

        sv1: SemanticVersion = SemanticVersion(GOOD_BUILD_NUMBER)
        sv2: SemanticVersion = SemanticVersion(f'{GOOD_BASIC_VERSION}+.5989')

        self.assertNotEqual(sv1, sv2, 'These should NOT be the same semantic version with a build number')

    def testMajorMinorPatchPreReleaseEqual(self):

        sv1: SemanticVersion = SemanticVersion(GOOD_PRE_RELEASE)
        sv2: SemanticVersion = SemanticVersion(GOOD_PRE_RELEASE)

        self.assertEqual(sv1, sv2, 'These should be the same semantic version with a pre-release value')

    def testMajorMinorPatchPreReleaseNotEqual(self):

        sv1: SemanticVersion = SemanticVersion(GOOD_BASIC_VERSION)
        sv2: SemanticVersion = SemanticVersion('7.0.0-Beta.1.0.0')

        self.assertNotEqual(sv1, sv2, 'These should NOT be the same semantic version with a pre-release value')

    def testMajorMinorPatchPreReleaseLessThan(self):

        sv1: SemanticVersion = SemanticVersion('7.0.0-Beta.1.0.0')
        sv2: SemanticVersion = SemanticVersion('7.0.0-Beta.1.0.1')

        self.assertLess(sv1, sv2, f'{sv1} should less than {sv2}')

    def testMajorMinorPatchLessThan(self):
        sv1: SemanticVersion = SemanticVersion(GOOD_PREVIOUS_BASIC_VERSION)
        sv2: SemanticVersion = SemanticVersion(GOOD_BASIC_VERSION)

        self.assertLess(sv1, sv2, 'The previous version must be less')

    def testPreReleaseLessThan(self):

        sv1: SemanticVersion = SemanticVersion('6.0.0-1.2')
        sv2: SemanticVersion = SemanticVersion('6.0.0-1.3')

        self.assertLess(sv1, sv2, 'The pre-release version must be less')

    def testPreReleaseGreaterThan(self):

        sv1: SemanticVersion = SemanticVersion('6.0.0-1.4')
        sv2: SemanticVersion = SemanticVersion('6.0.0-1.3')

        self.assertGreater(sv1, sv2, 'The pre-release version must be less')

    def testBuildNumberLessThan(self):

        sv1: SemanticVersion = SemanticVersion(f'{GOOD_BASIC_VERSION}+.5800')
        sv2: SemanticVersion = SemanticVersion(f'{GOOD_BASIC_VERSION}+.5988')

        self.assertLess(sv1, sv2, 'The build number IS less')

    def testBuildNumberGreaterThan(self):

        sv1: SemanticVersion = SemanticVersion(f'{GOOD_BASIC_VERSION}+.6000')
        sv2: SemanticVersion = SemanticVersion(f'{GOOD_BASIC_VERSION}+.5988')

        self.assertGreater(sv1, sv2, 'The build number IS less')

    def testIsSequenceLessTrue(self):

        sv1: SemanticVersion = SemanticVersion('7.0.0-Beta.1.0.0')

        seqLeft  = ['Beta', 1, 0, 0]
        seqRight = ['Beta', 1, 0, 1]

        ans: bool = sv1._isSequenceLess(seqLeft, seqRight)

        self.assertTrue(ans, 'Left sequence should be less')

    def testIsSequenceLessLeftIsNone(self):

        sv1: SemanticVersion = SemanticVersion('7.0.0-Beta.1.0.0')

        seqLeft  = ['Beta', 1, 0]
        seqRight = ['Beta', 1, 0, 1]

        ans: bool = sv1._isSequenceLess(seqLeft, seqRight)

        self.assertTrue(ans, 'Left sequence should be less')

    def testIsSequenceLessOnlyLeftIsInt(self):

        sv1: SemanticVersion = SemanticVersion('7.0.0-Beta.1.0.0')

        seqLeft  = ['Beta', 1, 0, 0]
        seqRight = ['Beta', 1, 0, 'a']

        ans: bool = sv1._isSequenceLess(seqLeft, seqRight)

        self.assertTrue(ans, 'Left sequence should be less')

    def testIsSequenceLessOnlyRightIsInt(self):

        sv1: SemanticVersion = SemanticVersion('7.0.0-Beta.1.0.0')

        seqLeft  = ['Beta', 1, 0, 'a']
        seqRight = ['Beta', 1, 0, 1]

        ans: bool = sv1._isSequenceLess(seqLeft, seqRight)

        self.assertFalse(ans, 'Left sequence is not less')

    def testIsSequenceLeftAlphaIsLess(self):

        sv1: SemanticVersion = SemanticVersion('7.0.0-Beta.1.0.0')

        seqLeft  = ['Beta', 1, 0, 'a']
        seqRight = ['Beta', 1, 0, 'b']

        ans: bool = sv1._isSequenceLess(seqLeft, seqRight)

        self.assertTrue(ans, 'Left sequence is not less')

    def testIsSequenceRightAlphaIsLess(self):

        sv1: SemanticVersion = SemanticVersion('7.0.0-Beta.1.0.0')

        seqLeft  = ['Beta', 1, 0, 'b']
        seqRight = ['Beta', 1, 0, 'A']

        ans: bool = sv1._isSequenceLess(seqLeft, seqRight)

        self.assertFalse(ans, 'Left sequence is not less')

    def testComparableTrue(self):

        sv1: SemanticVersion = SemanticVersion(GOOD_BASIC_VERSION)
        sv2: SemanticVersion = SemanticVersion(f'{GOOD_BASIC_VERSION}+.5988')

        actualValue: bool = sv1._comparable(other=sv2)

        self.assertTrue(actualValue, 'These should be comparable')

    def testComparableFalse(self):

        sv1: SemanticVersion      = SemanticVersion(GOOD_BASIC_VERSION)
        sve: SemanticVersionError = SemanticVersionError('I am not a SemanticVersion')

        actualValue: bool = sv1._comparable(other=sve)

        self.assertFalse(actualValue, 'These should NOT be comparable')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestSemanticVersion))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
