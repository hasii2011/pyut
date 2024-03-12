
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.SemanticVersion import SemanticVersion
from codeallybasic.UnitTestBase import UnitTestBase

from pyut.general.GitHubAdapter import GitHubAdapter


class TestGitHubAdapter(UnitTestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        UnitTestBase.setUpClass()

        import warnings
        # To ignore this warning:
        # GithubAdapter.py:60: ResourceWarning: unclosed <ssl.SSLSocket fd=5,
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    def setUp(self):
        super().setUp()
        self.githubAdapter: GitHubAdapter = GitHubAdapter()

    def tearDown(self):
        super().tearDown()
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

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestGitHubAdapter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
