from Lexical_Analyzer.LexicalAnalyzer import LexicalAnalyzer
#from Lexical_Analyzer.Token 
from Exception.CustomException import CustomException
from Parser.Parser import Parser 

def main():
    input_file_name = r"D:\RPAL_Interpreter\RPAL_Interpreter\test.txt"
    scanner = LexicalAnalyzer(input_file_name)
    
    try:
        tokens = scanner.scan()

        for token in tokens:
            print(f"<{token.type}, {token.value}>")

        
        # Parse the tokens to generate the Abstract Syntax Tree (AST)

        parser = Parser(tokens)
        AST = parser.parse()
        
        if AST is None:
            return
        
        # Convert the AST to string representation
        string_ast = parser.convert_AST_to_StringAST()
        
        for string in string_ast:
            print(string)
    
    except CustomException as e:
        print(e)


if __name__ == "__main__":
    main()
