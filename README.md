english
=======

A little experiment with Python bytecode. This is a Python to English "translator".

A lot of instructions are not yet supported (in particular if and for statements).

Objectives
----------

Examples
--------

```
from englishpython import *

def f(x):
    return x + 1

example = EnglishPython(f)
print(example)
```

TODO
----
- Add support for if, elif and else block

- Add support for indented outuput

- Drop the byteplay dependency (rewriting one of the dis functions)

- Add tests for EnglishByte and write tests for FakeRun

- Find a better name
