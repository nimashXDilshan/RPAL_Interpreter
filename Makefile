PYTHON = python

# Default target: runs the RPAL processor with the specified file
run:
	$(PYTHON) myrpal.py $(file)

# Target to print the AST
ast:
	$(PYTHON) myrpal.py -ast $(file) 

# Target to print the standardized AST
st:
	$(PYTHON) myrpal.py -st $(file) 

clean:
	rm -rf __pycache__ *.pyc

# Phony targets to avoid conflicts with files named 'run', 'ast', or 'sast'
.PHONY: run ast st