python-flavin
=============

Flavin is a tool to prune  all modules down to the minimal amount of code required to support a single top level python program.

Given a python program:

1. Traverse the imports gathering the python masters into a subdirectory.
2. Rename imports to point to these files.
3. Use vulture to find unused functions in these files.
4. Use ropetest to make copies of the python files without the unused code.

Thereby resulting in a minimal set of python code for loading into Micro Python.