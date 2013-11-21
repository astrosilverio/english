import byteplay
from collections import deque

from englishbyte import *


class FakeRun(object):
    """
    Class that "fake" runs the bytecode and create the translation during it.
    """
    tupledict = {'load': (0,1,0), 'store': (1,0,1), 'return': (1,0,1), 'binary': (2,1,1),
                'compare': (2,1,0)}

    def __init__(self, f):
        self.func = f
        self._code_obj = byteplay.Code.from_code(self.func.func_code)
        self.disassembly = self._code_obj.code
        self._python_stack = []
        self.bytedict = {'load': self.load, 'call': self.call, 'store': self.store,
                        'return': self.ret, 'binary': self.binary,
                        'compare': self.compare}
        self.english_stack = []
        self.run()

    def run(self):
        """
        """
        # How to handle line numbers?
        # The handling of command is a really ugly
        # Can we handle line numbers in command_type
        # Should command be a generator
        for command, args in self.instructions():
            #self.bytedict[command](args)
            self.call_byte(command, args)



    # Tuple order: (pop, append_to_python, append_to_english)
    def call(self, num_args):
        #(num_args+1,1,1)
        f_and_args = map(lambda x: x.short, self._python_stack[-(num_args+1):])
        self._python_stack = self._python_stack[:-(num_args+1)]
        call_string = EnglishByte('call', *f_and_args)
        self._python_stack.append(call_string)
        self.english_stack.append(call_string)

    def load(self, variable):
        # (0,1,0)
        load_string = EnglishByte('load', variable)
        self._python_stack.append(load_string)

    def store(self, variable):
        # (1,0,1)
        value = self._python_stack.pop().short
        store_string = EnglishByte('store', variable, value)
        self.english_stack.append(store_string)

    def ret(self, a_none):
        # (1,0,1)
        value = self._python_stack.pop().short
        ret_string = EnglishByte('return', value)
        self.english_stack.append(ret_string)

    def binary(self, operator):
        # (2,1,1)
        operand2 = self._python_stack.pop().short
        operand1 = self._python_stack.pop().short
        binary_string = EnglishByte('binary', operator, operand1, operand2)
        self._python_stack.append(binary_string)
        self.english_stack.append(binary_string)

    def compare(self, operator):
        # (2,1,0)
        # can be refactored with binary
        operand2 = self._python_stack.pop().short
        operand1 = self._python_stack.pop().short
        compare_string = EnglishByte('compare', operator, operand1, operand2)
        self._python_stack.append(compare_string)

    def call_byte(self, command, arg):
        # This is ugly
        if command != 'call':
            num_pop, num_stack, num_eng = self.tupledict[command]
        else:
            num_pop, num_stack, num_eng = (arg+1, 1, 1)
        pops = deque()
        for _ in range(num_pop):
            pops.appendleft(self._python_stack.pop().short)
        byte_string = EnglishByte(command, arg, *pops)
        # num_stack and num_eng are 0 or 1
        if num_stack:
            self._python_stack.append(byte_string)
        if num_eng:
            self.english_stack.append(byte_string)


    def instructions(self):
        for line in self.disassembly:
            com, args = line
            com = str(com)
            if com == 'SetLineno':
                self.line_number = str(args)
                continue

            command_type = com[:com.find('_')].lower()
            if command_type not in self.bytedict:
                print("We don't support {} yet.".format(com))
                raise KeyError
            elif command_type == 'binary':
                arguments = com[com.index('_') + 1:].lower()
            else:
                arguments = args
            yield command_type, arguments
