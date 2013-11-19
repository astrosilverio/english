import byteplay
import pdb


class FakeRun(object):

    def __init__(self, f):
        self.func = f
        self._pythonstack = []
        self._englishstack = []
        self._code_obj = byteplay.Code.from_code(self.func.func_code)
        self.disassembly = self._code_obj.code
        self.bytedict = {'load': self.load, 'call': self.call, 'store': self.store, 'return': self.ret,\
                         'binary': self.binary}
        self.operdict = {'add': 'plus', 'subtract': 'minus', 'multiply': 'times', 'divide': 'divided by', 'power': 'raised to the power of', 'modulo': 'modulo', 'and': 'AND', 'or': 'OR', 'xor': 'XOR'}
                
    @property
    def englishstack(self):
        """
        Should this be a generator? Yield FTW :)
        """
        for line in self.disassembly:
            command, args = line
            command = str(command)
            if command == 'SetLineno':
                self._englishstack.append(str(args))
            else:
                try:
                    command, args = self.instruction_type(line)
                    self.bytedict[command](args)
                except KeyError:
                    print("We don't support {} yet.".format(command))
                    continue
        return self._englishstack

#    def pop_from_stack(self, pops): # takes number of things to pop
#        popped = self.pythonstack[-pops:]
#        self.pythonstack = self.pythonstack[:-pops]
#        return popped

    def call(self, num_args):
        f_and_args = self._pythonstack[-(num_args+1):]
        self._pythonstack = self._pythonstack[:-(num_args+1)]
        call_string = EnglishByte('call', f_and_args)
        self._pythonstack.append(call_string)
        self._englishstack.append(call_string)

    def load(self, variable):
        load_string = EnglishByte('load', variable)
        self._pythonstack.append(load_string)

    def store(self, variable):
        value = self._pythonstack.pop()
        store_string = EnglishByte('store', [variable, value])
        self._englishstack.append(store_string)

    def ret(self, thing):
        value = self._pythonstack.pop()
        ret_string = EnglishByte('return', value)
        self._englishstack.append(ret_string)

    def binary(self, operator):
        operand1 = self._pythonstack.pop()
        operand2 = self._pythonstack.pop()
        binary_string = EnglishByte('binary', [operator, operand1, operand2]) 
        self._pythonstack.append(binary_string)
        self._englishstack.append(binary_string)

    def instruction_type(self, line):
        com, args = line
        com = str(com)
        commands = ["LOAD", "CALL", "STORE", "RETURN"]
        for start in commands:
            if com.startswith(start):
                command =  start.lower()
                arguments = args
        if com.startswith("BINARY"):
            command = "binary"
            arguments = com[com.index('_') + 1:].lower(), args
        return command, arguments
        

class EnglishPython(object):

    def __init__(self, f):
        self.func = f
        # Remove the None from the list
        self.code_obj = byteplay.Code.from_code(self.func.func_code)
        self.disassembly = self.code_obj.code
        self.english_translation = FakeRun(self.func).englishstack

    def __str__(self):
        return '\n'.join(('\t'.join((str(l[0]), l[1])) for l in self.english_translation))

    def __repr__(self):
        return ' '.join((l[1] for l in self.english_translation))


class EnglishByte(object):

    translation = {'load': "{0}", 'call': "{0}", 'store': "Store {0} as {1}.",\
                            'return': "Return {0}.", 'binary': "{1} {0} {2}"}
                            
    operdict = {'add': 'plus', 'subtract': 'minus', 'multiply': 'times', 'divide': 'divided by', 'power': 'raised to the power of', 'modulo': 'modulo', 'and': 'AND', 'or': 'OR', 'xor': 'XOR'}
                            
    full_english_only = ['store', 'return']

    def __init__(self, command, *byte_args):
        self.command = command
        self.byte_args = byte_args
        if self.command == 'binary':
            self.byte_args[0] = operdict[self.byte_args[0]]
        self.formatted_string = self.translation[self.command].format(byte_args)
        self._stack_english = None
        self._full_english = None


    @property
    def full_english(self):
        if self.command == 'binary':
            result = ' '.join(('Compute', self.formatted_string))
        elif self.command == 'call':
            func_arg = self.byte_args[1:]
            if len(func_arg) == 0:
                suffix = 'no argument'
            elif len(func_arg) == 1:
                suffix = '{0} as argument'.format(func_arg)
            else:
                suffix = '{0} as arguments'.format(', '.join(str(func_arg)))
            result = 'Call {0} with {1}.'.format(self.formatted_string, suffix)
        elif self.command in full_english_only:
            result = self.formatted_string
        else:
            result = None
        self._full_english = result
        
    @property
    def stack_english(self):
        if self.command in full_english_only:
            self._stack_english = None
        else:
            self._stack_english = self.formatted_string

