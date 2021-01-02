from collections import Counter
from logging import Logger
from logging import getLogger
from typing import List
from typing import cast

from github import Github
from github.GitRelease import GitRelease
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from org.pyut.general.SemanticVersion import SemanticVersion


class GithubAdapter:

    ALL_ISSUES_INDICATOR:     str = 'All'
    OPEN_MILESTONE_INDICATOR: str = 'Open'
    OPEN_ISSUE_INDICATOR:     str = 'open'

    PYUT_REPOSITORY_SLUG:           str = 'hasii2011/PyUt'
    MY_LIST: List[str] = ['1', '2', '2', '0', '9', '7', 'a',
                          'b', '9', 'f', 'b', '3', '5', '4',
                          'b', '8', '8', 'e', 'b', '8', '4',
                          '9', '7', '0', 'f', '6', '9', '2',
                          '9', 'a', 'e', '4', '0', '4', '0',
                          '9', '9', 'e', 'd', '5']

    def __init__(self):

        self.logger:  Logger = getLogger(__name__)
        self._github: Github = Github(''.join(GithubAdapter.MY_LIST))

    def getLatestVersionNumber(self) -> SemanticVersion:

        repo: Repository = self._github.get_repo(GithubAdapter.PYUT_REPOSITORY_SLUG)
        self.logger.info(f'{repo.full_name=}')

        releases: PaginatedList = repo.get_releases()

        latestReleaseVersion: SemanticVersion = SemanticVersion('0.0.0')
        for release in releases:
            gitRelease: GitRelease = cast(GitRelease, release)

            releaseNumber: str = gitRelease.tag_name
            numPeriods: int = self._countPeriods(releaseNumber)
            if numPeriods < 2:
                releaseNumber = f'{releaseNumber}.0'

            releaseVersion: SemanticVersion = SemanticVersion(releaseNumber)
            self.logger.debug(f'{releaseVersion=}')
            if latestReleaseVersion < releaseVersion:
                latestReleaseVersion = releaseVersion

        return latestReleaseVersion

    def cleanUp(self):
        del self._github

    def _countPeriods(self, releaseNumber: str) -> int:

        cnt = Counter(list(releaseNumber))
        return cnt['.']
