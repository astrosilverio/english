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
        self.english_translation = map(lambda x: x.full, FakeRun(self.func).english_stack)
        self.create_num_tabs()
        
    def create_num_tabs(self):
        self.num_tab = {}
        tabs = 0
        line_num = self.func.func_code.co_firstlineno + 1
        for line in self.disassembly:
            if str(line[0]) == 'SetLineno':
                line_num = line[1]
            elif type(line[0]) == byteplay.Label:
                self.num_tab[line_num + 1] = tabs - 1
            # this is not the right thing to do
            elif str(line[0]).startswith('JUMP_FOR'):
                tabs -= 1
            elif type(line[1]) == byteplay.Label:
                self.num_tab[line_num] = tabs
                tabs += 1
            else:
                self.num_tab[line_num] = tabs
                continue
                
    def __str__(self):
        result = ''
        for line in self.english_translation:
            tabs = '\t'*(self.num_tab[line[0]] + 1)
            line_string = tabs.join((str(line[0]), line[1]))
            result = '\n'.join((result, line_string))
        return result

    def __repr__(self):
        return ' '.join((l[1] for l in self.english_translation))
