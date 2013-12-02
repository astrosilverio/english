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
        self.fix_end_else()

    def create_num_tabs(self):
        self.num_tabs = {}
        tabs = 0
        tabs_stack = []
        first_line = self.func.func_code.co_firstlineno
        for line in self.disassembly:
            if str(line[0]) == 'SetLineno':
                line_num = int(line[1]) - first_line + 1
            elif type(line[0]) == byteplay.Label:
                tabs_stack.append(line[0])
                self.num_tabs[line_num + 1] = tabs - (len(tabs_stack) - 1) // 2
            elif str(line[0]).startswith('POP_JUMP'):
                self.num_tabs[line_num] = tabs
                tabs_stack.append(line[1])
                tabs += 1
            elif str(line[0]).startswith('JUMP'):
                self.num_tabs[line_num] = tabs
                tabs_stack.append(line[1])
            else:
                self.num_tabs[line_num] = tabs
                continue

    def fix_end_else(self):
        end_line = max(self.num_tabs.keys()) + self.func.func_code.co_firstlineno - 1
        end_commands = [line for line in self.english_translation if int(line[0]) == end_line]
        if len(end_commands) > 1 and (end_line, "Else:") in end_commands:
            new_end = (end_line, ' '.join(["Finally,", end_commands[1:][0][1]]))
            for line in end_commands:
                self.english_translation.remove(line)
            self.english_translation.append(new_end)

    def __str__(self):
        result = ''
        first_line = self.func.func_code.co_firstlineno
        for line_num, line_text in self.english_translation:
            tabs = ' '
            tabs += '\t' * self.num_tabs[line_num - first_line + 1]
            line_num += self.func.func_code.co_firstlineno
            line_string = tabs.join((str(line_num), line_text))
            result = '\n'.join((result, line_string))
        return result

    def __repr__(self):
        return ' '.join((l[1] for l in self.english_translation))
