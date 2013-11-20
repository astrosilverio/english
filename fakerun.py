import byteplay
import pdb

from englishbyte import *


class FakeRun(object):
    """
    Class that "fake" runs the bytecode and create the translation during it.
    """

    def __init__(self, f):
        self.func = f
        self._code_obj = byteplay.Code.from_code(self.func.func_code)
        self.disassembly = self._code_obj.code
        self._python_stack = []
        self.bytedict = {'load': self.load, 'call': self.call, 'store': self.store,
                         'return': self.ret, 'binary': self.binary}
        self.english_stack = []
        self.run()

    def run(self):
        """
        """
        # How to handle line numbers?
        # The handling of command is a really ugly
        # Can we handle line numbers in command_type
        # Should command be a generator
        for line in self.disassembly:
            command, args = line
            command = str(command)
            if command == 'SetLineno':
                self.english_stack.append(str(args))
            else:
                try:
                    command, args = self.instruction_type(line)
                    self.bytedict[command](args)
                except KeyError:
                    print("We don't support {} yet.".format(command))
                    continue

#    def pop_from_stack(self, pops): # takes number of things to pop
#        popped = self.pythonstack[-pops:]
#        self.pythonstack = self.pythonstack[:-pops]
#        return popped

    def call(self, num_args):
        f_and_args = self._python_stack[-(num_args+1):]
        self._python_stack = self._python_stack[:-(num_args+1)]
        call_string = EnglishByte('call', f_and_args)
        self._python_stack.append(call_string)
        self.english_stack.append(call_string)

    def load(self, variable):
        load_string = EnglishByte('load', variable)
        self._python_stack.append(load_string)

    def store(self, variable):
        value = self._python_stack.pop()
        store_string = EnglishByte('store', variable, value)
        self.english_stack.append(store_string)

    def ret(self, a_none):
        value = self._python_stack.pop()
        ret_string = EnglishByte('return', value)
        self.english_stack.append(ret_string)

    def binary(self, operator):
        operand1 = self._python_stack.pop()
        operand2 = self._python_stack.pop()
        binary_string = EnglishByte('binary', operator, operand1, operand2) 
        self._python_stack.append(binary_string)
        self.english_stack.append(binary_string)

    def instruction_type(self, line):
        com, args = line
        com = str(com)
        commands = {"LOAD", "CALL", "STORE", "RETURN"}
        for start in commands:
            if com.startswith(start):
                command =  start.lower()
                arguments = args
        if com.startswith("BINARY"):
            command = "binary"
            arguments = com[com.index('_') + 1:].lower(), args
        return command, arguments
