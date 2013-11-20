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
            self.bytedict[command](args)


#    def pop_from_stack(self, pops): # takes number of things to pop
#        popped = self.pythonstack[-pops:]
#        self.pythonstack = self.pythonstack[:-pops]
#        return popped

    def call(self, num_args):
        f_and_args = map(lambda x: x.short, self._python_stack[-(num_args+1):])
        self._python_stack = self._python_stack[:-(num_args+1)]
        call_string = EnglishByte('call', *f_and_args)
        self._python_stack.append(call_string)
        self.english_stack.append(call_string)

    def load(self, variable):
        load_string = EnglishByte('load', variable)
        self._python_stack.append(load_string)

    def store(self, variable):
        value = self._python_stack.pop().short
        store_string = EnglishByte('store', variable, value)
        self.english_stack.append(store_string)

    def ret(self, a_none):
        value = self._python_stack.pop().short
        ret_string = EnglishByte('return', value)
        self.english_stack.append(ret_string)

    def binary(self, operator):
        operand2 = self._python_stack.pop().short
        operand1 = self._python_stack.pop().short
        binary_string = EnglishByte('binary', operator, operand1, operand2) 
        self._python_stack.append(binary_string)
        self.english_stack.append(binary_string)
        
    def compare(self, operator):
    	# can be refactored with binary
        operand2 = self._python_stack.pop().short
        operand1 = self._python_stack.pop().short
        compare_string = EnglishByte('compare', operator, operand1, operand2) 
        self._python_stack.append(compare_string)

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
