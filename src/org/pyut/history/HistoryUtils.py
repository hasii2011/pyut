
from logging import Logger
from logging import getLogger

from org.pyut.general.Globals import cmp

"""
    @author P. Dabrowski <przemek.dabrowski@destroy-display.com> (18.11.2005)
    
    This module defines the format of the serialized commands and command groups
    of PyUt's history (undo/redo).
    It gives also some tools to set keywords in the format automaticaly.
    
    The format is textual, based on 'tokens' (identifiers) which can have
    two forms (without the spaces):
    
        1) token_begin token_name token_end
        2) token_begin token_name token_assign token_value token_end
    
    Where token_begin, token_end and token_assign are special sequences of
    charcters defines in this module.
    
    * Token_name is a characters sequence freely choosen by the developer. But be carefull
    because some special sequences are defined below.
    * Token_value is only used with the second form of token. It allows setting a
    value to a token. A token value _cannot_ be similar partially or completely to a
    reserved sequence (see below)
    
    Normally, you should not use the first form, but the second one, for e.g. to
    deserialize data used by a command.
    
    To see how it works, please see `tests.UnitTestHistory`
"""

TOKEN_BEGIN = '<'
TOKEN_END   = '>'
"""
    for serialization :  token delimiters
"""

TOKEN_ASSIGN = "="
"""
    When a token has an assigned value, we use this symbol for serialization
"""

TOKEN_ESCAPE = "\\"
"""
    It is the escape sequence, used if the token name or value contains a control
    sequence e.g.  TOKEN_ASSIGN
"""

GROUP_BEGIN_ID = "BEGIN_COMMAND_GROUP"
GROUP_END_ID   = "END_COMMAND_GROUP"
"""
    To limit the begining and the end of a serialized commands group
"""

GROUP_COMMENT_ID = "GROUP_COMMENT"
"""
    to find the comment/description of a command group
"""

COMMAND_BEGIN_ID = "BEGIN_COMMAND"
COMMAND_END_ID   = "END_COMMAND"
"""
Attributes limit the begining and the end of a serialized command
"""
COMMAND_CLASS_ID  = "COMMAND_CLASS"
COMMAND_MODULE_ID = "COMMAND_MODULE"
"""
    Used in the deserialization to build the correct command
"""

CTRL_SEQUENCES = [TOKEN_ESCAPE, TOKEN_BEGIN, TOKEN_END, TOKEN_ASSIGN]
"""
    if a sequence contains a control sequence, TOKEN_ESCAPE should
    be added to at the begining of the control sequence.

    _NOTE:_   TOKEN_ESCAPE must be first in the list
"""
RESERVED_SEQUENCES = [GROUP_BEGIN_ID, GROUP_END_ID, GROUP_COMMENT_ID,
                      COMMAND_BEGIN_ID, COMMAND_END_ID, COMMAND_CLASS_ID,
                      COMMAND_MODULE_ID]
"""
    if a sequence contains a reserved sequence, an exception should be raised.
"""
HISTORY_FILE_NAME = "pyutHistory"
"""
    Defines the base name of the file which contains the serialized commands.
"""

hLogger: Logger = getLogger('HistoryUtils')


def makeToken(tokenId: str):
    """
    @param tokenId : name (identificator) of the token

    @return a token (string) that is standard for all histories.
    """
    # return TOKEN_BEGIN + tokenId + TOKEN_END
    return f'{TOKEN_BEGIN}{tokenId}{TOKEN_END}'


def makeValuatedToken(tokenId: str, value: str):
    """
    @return a valuated token (string) in the format of the history
    manager. Use it in the serialize method of a command, so that
    you can get it back with the getTokenValue method.
    Notes : Raise an exception if tokenId or value are partially or
    completly a reserved sequence.

    @param tokenId  name of the token
    @param value value of the token
    """

    # check if the value isn't a reserved sequence and
    # if it is the case we raise an exception
    for sequence in RESERVED_SEQUENCES:
        if value.find(sequence) > -1:
            raise RuntimeError("'" + sequence + "' is a reserved sequence.")

    # check if the value isn't a control sequence and
    # if it is the case, an escape sequence is added.
    for sequence in CTRL_SEQUENCES:
        value = value.replace(sequence, TOKEN_ESCAPE + sequence)

    return makeToken(tokenId + TOKEN_ASSIGN + value)


def getTokenValue(tokenId: str, serializedData: str) -> str:
    """
    The token has to be created by the `makeToken()` method.  Used in the deserialize method of
    a command to get back a value.

    Args:
        tokenId:    name of the token
        serializedData:  string which contains the information needed to deserialize a command

    Returns: The value (string) of the specified token extracted
    from the specified string.
    """
    # to not to work on the original    -- hasii note, is this true?
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
    # of the token name followed by the assignement token.
    startPos = value.find(tokenId)
    startPos = startPos + len(tokenId) + len(TOKEN_ASSIGN)
    # value = value[startPos : len(value)]

    # find the end position which is just before TOKEN_ASSIGN
    endPos = value.find(TOKEN_END, startPos)

    # check if there isn't a escape token before TOKEN_END what
    # would means that the TOKEN_END sequence is a part of the
    # value, so we check for the next TOKEN_END.
    while cmp(value[endPos - len(TOKEN_ESCAPE): endPos], TOKEN_ESCAPE) == 0:
        endPos = value.find(TOKEN_END, endPos + 1)
    value = value[startPos: endPos]

    # remove all the escape sequences
    value = value.replace(TOKEN_ESCAPE, "")
    # add simple escape sequences where they where double
    value = value.replace(tempEscape, TOKEN_ESCAPE)

    hLogger.info(f'return value: {value}')
    return value
