from enum import Enum

class TokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    OPERATOR = "OPERATOR"
    PUNCTUATION = "PUNCTUATION"
    STRING = "STRING"
    DELETE = "DELETE"
    END_OF_TOKENS = "EndOfTokens"
    