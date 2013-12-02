english
=======

A Python-to-English "translator" that takes Python code and returns English sentences.

How Does It Work?
-------------------

`english` first disassembles the source code into bytecode. Right now, we're doing this using `byteplay`. Then each line of bytecode is parsed and a brief description of the operation is generated.

Examples
--------

Check out our demos for specific examples of the type of output you can expect. In general, the expected usage is to create an `EnglishPython` object for the function you would like to translate. The `__str__` method of the `EnglishPython` object will print the translation, along with the line numbers of where each operation occurs in the source code. The `__repr__` method will join the lines of translation together as one string.

Currently Supported Operations
--------------------------------
- Function calls

- Binary operations

TODO
----
- Finish support for if, elif and else block (see if-else branch)

- Drop the byteplay dependency (rewriting one of the dis functions)