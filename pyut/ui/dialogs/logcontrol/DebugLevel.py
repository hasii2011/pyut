
from logging import DEBUG
from logging import ERROR
from logging import FATAL
from logging import INFO
from logging import NOTSET
from logging import WARNING

from enum import Enum


class DebugLevel(Enum):
    """
    A wrapper enumeration around Python log levels
    """

    NOT_SET = 'NOTSET'
    ERROR   = 'ERROR'
    WARNING = 'WARNING'
    INFO    = 'INFO'
    DEBUG   = 'DEBUG'
    FATAL   = 'FATAL'

    @classmethod
    def toEnum(cls, pythonLevel: int) -> 'DebugLevel':
        import logging

        match pythonLevel:
            case logging.NOTSET:
                return DebugLevel.NOT_SET
            case logging.ERROR:
                return DebugLevel.ERROR
            case logging.WARNING:
                return DebugLevel.WARNING
            case logging.INFO:
                return DebugLevel.INFO
            case logging.DEBUG:
                return DebugLevel.DEBUG
            case logging.FATAL:
                return DebugLevel.FATAL
            case _:
                return DebugLevel.NOT_SET

    @classmethod
    def toPythonLevel(cls, debugLevel: 'DebugLevel') -> int | None:

        match debugLevel:
            case DebugLevel.NOT_SET:
                return NOTSET
            case DebugLevel.ERROR:
                return ERROR
            case DebugLevel.WARNING:
                return WARNING
            case DebugLevel.INFO:
                return INFO
            case DebugLevel.DEBUG:
                return DEBUG
            case DebugLevel.FATAL:
                return FATAL
            case _:
                assert False, 'Developer error, unknown enumeration value'
