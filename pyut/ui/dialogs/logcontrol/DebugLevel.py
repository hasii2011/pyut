
from logging import DEBUG
from logging import ERROR
from logging import FATAL
from logging import INFO
from logging import NOTSET
from logging import WARNING

from enum import Enum


class DebugLevel(Enum):
    """
    A wrapper enumeration around Python log levels; The
    value is the Pythong logging level
    """

    NOTSET  = NOTSET
    ERROR   = ERROR
    WARNING = WARNING
    INFO    = INFO
    DEBUG   = DEBUG
    FATAL   = FATAL

    @classmethod
    def toEnum(cls, pythonLevel: int) -> 'DebugLevel':
        """
        This is needed when we retrieve the actual logger.  Need the
        enumeration so we can treat it as a
        Args:
            pythonLevel:

        Returns:

        """
        import logging

        match pythonLevel:
            case logging.NOTSET:
                return DebugLevel.NOTSET
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
                return DebugLevel.NOTSET
