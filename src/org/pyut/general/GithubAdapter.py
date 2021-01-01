from collections import Counter
from logging import Logger
from logging import getLogger
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

    USER_NAME:                      str = 'hasii2011'
    READ_ONLY_AUTHENTICATION_TOKEN: str = '935fe2465886111895ae64e1e06d9e7fc0b72e25'
    PYUT_REPOSITORY_SLUG:           str = 'hasii2011/PyUt'

    """
    Ok, hackers.  I locked down this token so all you can do is read my public repositories;
    """

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._userName:            str    = GithubAdapter.USER_NAME
        self._authenticationToken: str    = GithubAdapter.READ_ONLY_AUTHENTICATION_TOKEN
        self._github:              Github = Github(login_or_token=self._authenticationToken)

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
