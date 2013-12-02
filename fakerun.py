import byteplay
from collections import deque

from englishbyte import EnglishByte


class FakeRun(object):
    """
    Class that "fake" runs the bytecode and create the translation during it.
    """

    # Tuple order: (pop, append_to_python, append_to_english)
    tupledict = {'load': (0,1,0), 'store': (1,0,1), 'return': (1,0,1),
                 'binary': (2,1,1), 'compare': (2,1,0), 'call': (1, 1, 1),
                 'else': (0,0,1), 'pop': (1,0,1)}

    def __init__(self, f):
        self.func = f
        self._code_obj = byteplay.Code.from_code(self.func.func_code)
        self.disassembly = self._code_obj.code
        self._python_stack = []
        self._loops = []
        self.english_stack = []
        self.run()

    def run(self):
        """
        """
        # How to handle line numbers?
        # Can we handle line numbers in command_type
        for command, arg in self.instructions():
            self.call_byte(command, arg)

    def call_byte(self, command, arg):
        if command == 'call': # num_pop should be arg + 1
            num_pop, num_stack, num_eng = (arg + 1, 1, 1)
        else:
            num_pop, num_stack, num_eng = self.tupledict[command]
        pops = deque()
        for _ in range(num_pop):
            pops.appendleft(self._python_stack.pop().short)
        byte_string = EnglishByte(command, self.line_num, 0, arg, *pops)
        # num_stack and num_eng are 0 or 1
        if num_stack:
            self._python_stack.append(byte_string)
        if num_eng:
            self.english_stack.append(byte_string)

    def instructions(self):
        for line in self.disassembly:
            com_obj, byte_arg = line
            com = str(com_obj)
            if com == 'SetLineno':
                self.line_num = int(byte_arg)
                continue
            elif com.startswith('JUMP_'):
                self._loops.append(byte_arg)
                byte_arg = None
                continue
            elif com.startswith('POP_JUMP'):
                self._loops.append(byte_arg)
                byte_arg = None
            if isinstance(com_obj, byteplay.Label):
                if com_obj in self._loops:
                    self._loops.remove(com_obj)
                    com = 'else_'
                    self.line_num = self.line_num + 1
                else:
                    continue
                
            command_type = com[:com.find('_')].lower()
            if command_type not in self.tupledict:
                print("We don't support {} yet.".format(com))
                raise KeyError
            elif command_type == 'binary':
                argument = com[com.index('_') + 1:].lower()
            else:
                argument = byte_arg
            yield command_type, argument
