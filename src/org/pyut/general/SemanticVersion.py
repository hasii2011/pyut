
from typing import List
from typing import Sequence
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from re import Match as regexMatch
from re import compile as regexCompile

from itertools import zip_longest as iZipLongest


class SemanticVersionError(Exception):
    pass


class SemanticVersion:
    """
    Inspired by https://github.com/keleshev/version

    A normal version number MUST take the form X.Y.Z where
    X, Y, and Z are non-negative integers. X is the major
    version, Y is the minor version, and Z is the patch
    version. Each element MUST increase numerically by
    increments of one. For instance: 6.9.0 -> 6.10.0 ->
    6z.11.0.

    A pre-release version MAY be denoted by appending a dash
    and a series of dot separated identifiers immediately
    following the patch version. Identifiers MUST be
    comprised of only ASCII alphanumerics and dash
    [0-9A-Za-z-].

    A build version MAY be denoted by appending a plus sign
    and a series of dot separated identifiers immediately
    following the patch version or pre-release version.
    Identifiers MUST be comprised of only ASCII
    alphanumerics and dash [0-9A-Za-z-].

    When a major version number is incremented, the minor
    version and patch version MUST be reset to zero. When a
    minor version number is incremented, the patch version
    MUST be reset to zero. For instance: 6.1.3 -> 7.0.0 and
    8.1.7 -> 8.2.0.

    """
    def __init__(self, version: str):

        self.logger: Logger = getLogger(__name__)

        self._re = regexCompile('^'
                                '(\d+)\.(\d+)\.(\d+)'     # minor, major, patch
                                '(-[0-9A-Za-z-\.]+)?'     # pre-release
                                '(\+[0-9A-Za-z-\.]+)?'    # build
                                '$')

        match: regexMatch = self._re.match(version)     # type: ignore
        if match is None:
            raise SemanticVersionError(f'Invalid Version: `{version}`')

        mGroups: Sequence[str] = match.groups()

        self.major: int = int(mGroups[0])
        self.minor: int = int(mGroups[1])
        self.patch: int = int(mGroups[2])

        self.preRelease: List[Union[int, str]] = self._makeGroup(match.group(4))
        self.build:      List[Union[int, str]] = self._makeGroup(match.group(5))

    def _majorMinorPatch(self) -> List[int]:
        return [self.major, self.minor, self.patch]

    def _makeGroup(self, g: str) -> List[Union[int, str]]:
        if g is None:
            return []
        else:
            return list(map(SemanticVersion.safeInt, g[1:].split('.')))

    @staticmethod
    def safeInt(s):
        assert type(s) is str
        try:
            return int(s)
        except ValueError:
            return s

    def __eq__(self, alien: object):

        if self._comparable(alien) is False:
            return False
        else:
            other: SemanticVersion = cast(SemanticVersion, alien)
            return all([self._majorMinorPatch() == other._majorMinorPatch(),
                        self.build == other.build,
                        self.preRelease == other.preRelease])

    def __lt__(self, other):

        if self._comparable(other) is False:
            return False

        # noinspection PyProtectedMember
        if self._majorMinorPatch() == other._majorMinorPatch():

            if self.preRelease == other.preRelease:
                if self.build == other.build:
                    return False
                elif self.build and other.build:
                    return self._isSequenceLess(self.build, other.build)
                elif self.build or other.build:
                    return bool(other.build)
                assert False, 'Should not be reachable'
            elif self.preRelease and other.preRelease:
                return self._isSequenceLess(self.preRelease, other.preRelease)
            elif self.preRelease or other.preRelease:
                return bool(self.preRelease)
            assert False, 'Should not be reachable'
        else:
            # noinspection PyProtectedMember
            return self._majorMinorPatch() < other._majorMinorPatch()

    def __gt__(self, other):
        if not self < other and not self == other:
            return True
        else:
            return False

    def _isSequenceLess(self, left, right) -> bool:

        assert {int, str} >= set(map(type, right))

        for lStr, rStr in iZipLongest(left, right):
            assert not (lStr is None and rStr is None)

            if lStr is None or rStr is None:
                return bool(lStr is None)

            if type(lStr) is int and type(rStr) is int:
                if lStr < rStr:
                    return True
            elif type(lStr) is int or type(rStr) is int:
                return type(lStr) is int
            elif lStr != rStr:
                return lStr < rStr
        return False

    def _comparable(self, other: object) -> bool:

        if isinstance(other, SemanticVersion):
            return True
        else:
            return False

    def __str__(self):
        mmp: List[int] = self._majorMinorPatch()
        s:   str       = f'{str(mmp[0])}.{str(mmp[1])}.{str(mmp[2])}'

        if len(self.preRelease) > 0:
            s += '-%s' % '.'.join(str(s) for s in self.preRelease)
        if len(self.build) > 0:
            s += '+%s' % '.'.join(str(s) for s in self.build)
        return s

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__str__())
