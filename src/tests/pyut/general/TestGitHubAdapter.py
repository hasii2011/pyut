
from logging import Logger
from logging import getLogger
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from pyut.general.SemanticVersion import SemanticVersion

from pyut.preferences.PyutPreferences import PyutPreferences

from tests.TestBase import TestBase

from pyut.general.GitHubAdapter import GitHubAdapter


class TestGitHubAdapter(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGitHubAdapter.clsLogger = getLogger(__name__)
        PyutPreferences.determinePreferencesLocation()

        import warnings
        # To ignore this warning:
        # GithubAdapter.py:60: ResourceWarning: unclosed <ssl.SSLSocket fd=5,
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    def setUp(self):
        self.logger:        Logger        = TestGitHubAdapter.clsLogger
        self.githubAdapter: GitHubAdapter = GitHubAdapter()

    def tearDown(self):
        self.githubAdapter.cleanUp()
        del self.githubAdapter

    def testGetLatestVersionNumber(self):
        try:
            latestReleaseNumber: SemanticVersion = self.githubAdapter.getLatestVersionNumber()
            self.logger.info(f'Pyut latest release number: {latestReleaseNumber}')
        except (ValueError, Exception) as e:
            self.logger.error(f'{e}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGitHubAdapter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
