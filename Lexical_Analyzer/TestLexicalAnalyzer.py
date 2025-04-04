from Lexical_Analyzer.LexicalAnalyzer import LexicalAnalyzer
from Exception.CustomException import CustomException


def main():
    
    input_file_name = r"D:\RPAL_Interpreter\RPAL_Interpreter"

    scanner = LexicalAnalyzer(input_file_name)
    
    try:
        tokens = scanner.scan()
        
        # Print the generated tokens
        for token in tokens:
            print(f"<{token.type}, {token.value}>")
    except CustomException as e:
        print(e)

if __name__ == "__main__":
    main()
