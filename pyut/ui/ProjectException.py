
from enum import Enum

from pyut.ui.IPyutProject import IPyutProject


class ProjectExceptionType(Enum):
    INVALID_PROJECT   = 'Invalid Project'
    PROJECT_NOT_FOUND = 'Project Not Found'
    ATTRIBUTE_ERROR   = 'Attribute Error'
    TYPE_ERROR        = 'Type Error'
    ASSERTION_ERROR   = 'Assertion Error'
    GENERAL_ERROR     = 'General Error'


class ProjectException(Exception):

    def __init__(self, exceptionType: ProjectExceptionType, message: str, project: IPyutProject):

        self._exceptionType: ProjectExceptionType = exceptionType

        self._message:    str = message
        self._badProject: IPyutProject = project

    @property
    def message(self) -> str:
        return self._message

    @property
    def project(self) -> IPyutProject:
        return self._badProject

    @property
    def exceptionType(self) -> ProjectExceptionType:
        return self._exceptionType

    def __str__(self) -> str:
        return f'{self._message}'
