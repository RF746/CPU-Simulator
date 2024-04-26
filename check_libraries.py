# List of library names to import
libraries = ['numpy', 'queue', 'sys', 'math', 'random', 'matplotlib', 'itertools']

# Iterate over each library name
for lib in libraries:
    try:
        # Try to import the library
        __import__(lib)
        # If successful, print a success message
        print(f"Successfully imported {lib}.")
    except ImportError:
        # If import failed, print a failure message
        print(f"Failed to import {lib}.")
