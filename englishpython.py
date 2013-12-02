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
#            elif str(line[0]).startswith('JUMP_ABS'):
#                tabs -= 1
            elif type(line[1]) == byteplay.Label and not str(line[0]).startswith('JUMP_'):
                self.num_tab[line_num] = tabs
                tabs += 1
            elif str(line[0]).startswith('JUMP_ABS'):
                self.num_tab[line_num] = tabs
            else:
                self.num_tab[line_num] = tabs
                continue
                
#     def create_num_tabs(self):
#         self.num_tab = {}
#         tabs = 0
#         line_num = self.func.func_code.co_firstlineno + 1
#         for line_num, line_text in self.english_translation:
#             if line[0] != str(line_num):
#                 line_num = line[0]
#             if line_text.startswith('If') or line_text.startswith('Else'):
#                 self.num_tab[line_num] = tabs
#                 tabs += 1
            
    def __str__(self):
        result = ''
        for line in self.english_translation:
            tabs = ' '
            tabs += '\t'*(self.num_tab[line[0]])
            line_string = tabs.join((str(line[0]), line[1]))
            result = '\n'.join((result, line_string))
        return result

    def __repr__(self):
        return ' '.join((l[1] for l in self.english_translation))
