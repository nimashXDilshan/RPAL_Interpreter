from Engine.Evaluator import Evaluvator

def main():
    """Main function that handles command line arguments and runs the evaluator"""
    import sys
    
    # Default values // if no fn value provide in the argument please use fn= "test.txt" file
    fn = "test.txt"
    is_print_ast = False
    is_print_st = False
    
    args = sys.argv[1:]  # Skip the script name
    
    if len(args) == 0:
        fn = "test.txt"
        is_print_ast = True
        is_print_st = True
    elif len(args) == 3 and (
        (args[0].lower() == "-ast" and args[1].lower() == "-st") or
        (args[0].lower() == "-st" and args[1].lower() == "-ast")
    ):
        fn = args[2]
        is_print_ast = True
        is_print_st = True
    elif len(args) == 2:
        fn = args[1]
        if args[0].lower() == "-ast":
            is_print_ast = True
        elif args[0].lower() == "-st":
            is_print_st = True
        else:
            print("Invalid Arguments Passing!")
            return
    elif len(args) == 1:
        fn = args[0]
    else:
        print("Invalid Arguments Passing!")
        return
    
    # Call the evaluvate function in the Evaluator class and print the result # fn->file_name 
    print(Evaluvator.evaluvate(fn, is_print_ast, is_print_st))

if __name__ == "__main__":
    main()

    