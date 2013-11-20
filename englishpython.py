import byteplay

from fakerun import *

class EnglishPython(object):
    """
    Wrapper class, takes an function and return its bytecode
    """

    def __init__(self, f):
        self.func = f
        # Remove the None from the list
        self.code_obj = byteplay.Code.from_code(self.func.func_code)
        self.disassembly = self.code_obj.code
        self.english_translation = FakeRun(self.func).english_stack

    def __str__(self):
        return '\n'.join((l.full for l in self.english_translation))

    def __repr__(self):
        return ' '.join((l for l in self.english_translation))
