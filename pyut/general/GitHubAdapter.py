
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from collections import Counter

from semantic_version import Version as SemanticVersion

from github import Github
from github.GitRelease import GitRelease
from github.PaginatedList import PaginatedList
from github.Repository import Repository


class GitHubAdapter:

    ALL_ISSUES_INDICATOR:     str = 'All'
    OPEN_MILESTONE_INDICATOR: str = 'Open'
    OPEN_ISSUE_INDICATOR:     str = 'open'

    PYUT_REPOSITORY_SLUG:   str       = 'hasii2011/PyUt'
    MY_LIST:                List[str] = ['g', 'h', 'p', '_', 'B',
                                         'i', 'M', 'm', 'Z', 'N',
                                         's', '1', 'U', 'A', 'o',
                                         's', 'o', 'V', '6', 'a',
                                         'c', 'r', 'U', '1', 'o',
                                         'B', 'H', 'e', 'x', 'I',
                                         'r', 'S', 'x', 'H', '2',
                                         '8', 'K', 'z', 'Z', 'W']

    def __init__(self):

        self.logger:  Logger = getLogger(__name__)
        self._github: Github = Github(''.join(GitHubAdapter.MY_LIST))

    def getLatestVersionNumber(self) -> SemanticVersion:

        repo: Repository = self._github.get_repo(GitHubAdapter.PYUT_REPOSITORY_SLUG)
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
