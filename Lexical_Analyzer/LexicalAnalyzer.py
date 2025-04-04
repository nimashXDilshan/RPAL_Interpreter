import re
#from enum import Enum
from Exception.CustomException import CustomException
from Lexical_Analyzer.Token import Token
from Lexical_Analyzer.TokenType import TokenType


class LexicalAnalyzer:
    def __init__(self, input_file_name):
        self.input_file_name = input_file_name
        self.tokens = []
    
    def scan(self):
        try:
            with open(self.input_file_name, 'r') as file:
                lines = file.readlines()
                for line_count, line in enumerate(lines, start=1):
                    try:
                        self.tokenize_line(line)
                    except CustomException as e:
                        raise CustomException(f"{e} in LINE: {line_count}\nERROR in lexical_analysis.")
        except IOError as e:
            print(f"File error: {e}")
        
        return self.tokens

    def tokenize_line(self, line):
        digit = "[0-9]"
        letter = "[a-zA-Z]"
        operator_symbol = re.compile(r"[+\-*/<>&.@/:=~|$!#%^_\[\]{}\"`\\?]")
        escape = re.compile(r"(\\\\'|\\\\t|\\\\n|\\\\\\\\)")
        
        identifier_pattern = re.compile(f"{letter}({letter}|{digit}|_)*")
        integer_pattern = re.compile(f"{digit}+")
        operator_pattern = re.compile(r"[+\-*/<>&.@/:=~|$!#%^_\[\]{}\"`\\?]+")
        punctuation_pattern = re.compile(r"[(),;]")
        spaces_pattern = re.compile(r"(\s|\t)+")
        string_pattern = re.compile(r"'([a-zA-Z0-9+\-*/<>&.@/:=~|$!#%^_\[\]{}\"`\\?\\\\'\\\\t\\\\n\\\\\\\\(),;\s]*)'")
        comment_pattern = re.compile(r"//.*")

        current_index = 0
        while current_index < len(line):
            current_char = line[current_index]
            
            if comment_pattern.match(line[current_index:]):
                break
            
            if spaces_pattern.match(line[current_index:]):
                current_index += len(spaces_pattern.match(line[current_index:]).group())
                continue
            
            if identifier_pattern.match(line[current_index:]):
                identifier = identifier_pattern.match(line[current_index:]).group()
                keywords = {"let", "in", "fn", "where", "aug", "or", "not", "gr", "ge", "ls", 
                            "le", "eq", "ne", "true", "false", "nil", "dummy", "within", "and", "rec"}
                token_type = TokenType.KEYWORD if identifier in keywords else TokenType.IDENTIFIER
                self.tokens.append(Token(token_type, identifier))
                current_index += len(identifier)
                continue
            
            if integer_pattern.match(line[current_index:]):
                integer = integer_pattern.match(line[current_index:]).group()
                self.tokens.append(Token(TokenType.INTEGER, integer))
                current_index += len(integer)
                continue
            
            if operator_pattern.match(line[current_index:]):
                operator = operator_pattern.match(line[current_index:]).group()
                self.tokens.append(Token(TokenType.OPERATOR, operator))
                current_index += len(operator)
                continue
            
            if string_pattern.match(line[current_index:]):
                string = string_pattern.match(line[current_index:]).group()
                self.tokens.append(Token(TokenType.STRING, string))
                current_index += len(string)
                continue
            
            if punctuation_pattern.match(current_char):
                self.tokens.append(Token(TokenType.PUNCTUATION, current_char))
                current_index += 1
                continue
            
            raise CustomException(f"Unable to tokenize CHARACTER: {current_char} at INDEX: {current_index}")
