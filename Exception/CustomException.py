import re
from enum import Enum

class CustomException(Exception):
    def __init__(self, message=None, cause=None):
        super().__init__(message)
        self.cause = cause