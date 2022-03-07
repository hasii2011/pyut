
from typing import List

from logging import Logger
from logging import getLogger

from org.pyut.general.Globals import cmp

"""
   
    This module defines the format of the serialized commands and command groups
    for PyUt history (undo/redo).
    It provides some tools to automatically set keywords in the format.
    
    The format is textual, based on 'tokens' (identifiers) which can have
    two forms (without the spaces):
    
        1) token_begin token_name token_end
        2) token_begin token_name token_assign token_value token_end
    
    Where token_begin, token_end and token_assign are special sequences of
    characters defined in this module.
    
    * Token_name is a characters sequence freely chosen by the developer. But be careful
    because some special sequences are defined below.
    * Token_value is only used with the second form of token. It allows setting a
    value to a token. A token value _cannot_ be similar partially or completely to a
    reserved sequence (see below)
    
    Normally, you should not use the first form, but the second one, for e.g. to
    deserialize data used by a command.
    
    To see how this works, please see `tests.UnitTestHistory`
"""

TOKEN_BEGIN: str = '<'
TOKEN_END:   str = '>'
"""
    for serialization :  token delimiters
"""
TOKEN_ASSIGN: str = "="
"""
    When a token has an assigned value, we use this symbol for serialization
"""
TOKEN_ESCAPE: str = "\\"
"""
    It is the escape sequence, used if the token name or value contains a control
    sequence e.g.  TOKEN_ASSIGN
"""
GROUP_BEGIN_ID: str = "BEGIN_COMMAND_GROUP"
GROUP_END_ID:   str = "END_COMMAND_GROUP"
"""
    To limit the beginning and the end of a serialized commands group
"""
GROUP_COMMENT_ID: str = "GROUP_COMMENT"
"""
    to find the comment/description of a command group
"""
COMMAND_BEGIN_ID: str = "BEGIN_COMMAND"
COMMAND_END_ID:   str = "END_COMMAND"
"""
Attributes limit the beginning and the end of a serialized command
"""
COMMAND_CLASS_ID:  str  = "COMMAND_CLASS"
COMMAND_MODULE_ID: str = "COMMAND_MODULE"
"""
    Used in the deserialization to build the correct command
"""
CTRL_SEQUENCES: List[str] = [TOKEN_ESCAPE, TOKEN_BEGIN, TOKEN_END, TOKEN_ASSIGN]
"""
    if a sequence contains a control sequence, TOKEN_ESCAPE should
    be added at the beginning of the control sequence.

    _NOTE:   TOKEN_ESCAPE must be first in the list
"""
RESERVED_SEQUENCES: List[str] = [GROUP_BEGIN_ID, GROUP_END_ID, GROUP_COMMENT_ID,
                                 COMMAND_BEGIN_ID, COMMAND_END_ID, COMMAND_CLASS_ID, COMMAND_MODULE_ID]
"""
    if a sequence contains a reserved sequence, an exception should be raised.
"""
HISTORY_FILE_NAME: str = "pyutHistory"
"""
    Defines the base name of the file which contains the serialized commands.
"""
hLogger: Logger = getLogger('HistoryUtils')


def tokenize(tokenId: str):
    """

    Args:
        tokenId:     name (identifier) of the token

    Returns:    a token (string) that is standard for all histories.
    """
    return f'{TOKEN_BEGIN}{tokenId}{TOKEN_END}'


def tokenizeValue(tokenId: str, value: str):
    """
    Use it in the serialize method of a command, so that
    you can get it back with the getTokenValue method.

    Args:
        tokenId:    name of the token
        value:      value of the token

    Returns:    a valuated token (string) in the format of the history manager.

    Raise an exception if tokenId or value are partially or
    completely a reserved sequence.
    """
    #
    # check if the value isn't a reserved sequence and
    # if it is the case we raise an exception
    for sequence in RESERVED_SEQUENCES:
        if value.find(sequence) > -1:
            raise RuntimeError(f"{sequence}  is a reserved sequence.")
    #
    # check if the value isn't a control sequence and
    # if it is the case, an escape sequence is added.
    for sequence in CTRL_SEQUENCES:
        value = value.replace(sequence, TOKEN_ESCAPE + sequence)

    return tokenize(tokenId + TOKEN_ASSIGN + value)


def deTokenize(tokenId: str, serializedData: str) -> str:
    """
    The token has to be created by the `tokenize()` method.  Used in the deserialize method of
    a command to get back a value.

    Args:
        tokenId:    name of the token
        serializedData:  string which contains the information needed to deserialize a command

    Returns: The value (string) of the specified token extracted from the specified string.
    """
    # to not work on the original    -- hasii note, is this true?
    value = serializedData
    hLogger.info(f'tokenId: `{tokenId}`')
    hLogger.debug(f'value: {value}')
    # find a char that is not present in the value
    tempEscape = chr(1)
    while value.find(tempEscape) > -1:
        tempEscape = chr(ord(tempEscape + str(1)))

    # replace the double escape sequences by a char that is not
    # present in the original value
    value = value.replace(TOKEN_ESCAPE + TOKEN_ESCAPE, tempEscape)

    # find the start position of the value which is just after the end
    # of the token name followed by the assignment token.
    startPos = value.find(tokenId)
    startPos = startPos + len(tokenId) + len(TOKEN_ASSIGN)
    # value = value[startPos : len(value)]

    # find the end position which is just before TOKEN_ASSIGN
    endPos = value.find(TOKEN_END, startPos)

    # check if there is not an escape token before TOKEN_END what
    # would mean that the TOKEN_END sequence is a part of the
    # value, so we check for the next TOKEN_END.
    while cmp(value[endPos - len(TOKEN_ESCAPE): endPos], TOKEN_ESCAPE) == 0:
        endPos = value.find(TOKEN_END, endPos + 1)
    value = value[startPos: endPos]

    # remove all the escape sequences
    value = value.replace(TOKEN_ESCAPE, "")
    # add simple escape sequences where they were double
    value = value.replace(tempEscape, TOKEN_ESCAPE)

    hLogger.info(f'return value: {value}')
    return value
