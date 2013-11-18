import byteplay
import pdb


class FakeRun(object):

    def __init__(self, f):
        self.func = f
        self.stack = []
        self.code_obj = byteplay.Code.from_code(self.func.func_code)
        self.disassembly = self.code_obj.code
        self.bytedict = {'load': self.load, 'call': self.call, 'store': self.store, 'return': self.ret,\
                         'binary': self.binary}
        self.translation = {'load': None, 'call': "Call {0} with {1}", 'store': "Store {0} as {1}.",\
                            'return': "Return {0}.", 'binary': "Compute {0}."}
        self.operdict = {'add': 'plus', 'subtract': 'minus', 'multiply': 'times', 'divide': 'divided by'}


    def step_through_bytecode(self):
        """
        Should this be a generator? Yiel FTW :)
        """
        result = []
        for line in self.disassembly:
            command, args = line
            command = str(command)
            if command == 'SetLineno':
                line_num = args
            else:
                try:
                    command, args = self.instruction_type(line)
                    args_names = self.bytedict[command](args)
                except KeyError:
                    print("We don't support {} yet.".format(command))
                    continue
                line_translation = self.translate(command, args_names)
                result.append((line_num, line_translation))
        return result

    #def pop_and_push(self, pops, pushes, *byte_args):
        #poped = self.stack[-pops:]
        #self.stack

    def call(self, num_args):
        f_and_args = self.stack[-(num_args+1):]
        self.stack = self.stack[:-(num_args+1)]
        stack_string = 'result of call to {}'.format(f_and_args[0])
        self.stack.append(stack_string)
        return f_and_args

    def load(self, thing):
        self.stack.append(thing)
        return []

    def store(self, thing):
        return [self.stack.pop(), thing]

    def ret(self, thing):
        return [self.stack.pop()]

    def binary(self, operator):
        operator = operator[0]
        operand1 = self.stack.pop()
        operand2 = self.stack.pop()
        operation = self.operdict[operator]
        stack_string = 'result of {0} {1} {2}'.format(operand1, operation, operand2)
        self.stack.append(stack_string)
        return '{0} {1} {2}'.format(operand1, operation, operand2)

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

    def translate(self,command, arg_names):
        if not arg_names:
            return self.translation[command]
        elif command == 'binary':
            return self.translation[command].format(arg_names)
        elif command == 'return':
            return self.translation[command].format(arg_names[0])
        elif command == 'store':
            return self.translation[command].format(arg_names[0], arg_names[1])
        elif command == 'call' and len(arg_names) == 1:
            return self.translation[command].format(arg_names[0], 'no argument.')
        elif command == 'call' and len(arg_names) == 2:
            return self.translation[command].format(arg_names[0], ' '.join([str(arg_names[1]),'as argument.']))
        elif command == 'call' and len(arg_names) > 2:
            arg_string = ' '.join([' and '.join(map(str, arg_names[1:])), 'as arguments.'])
            return self.translation[command].format(arg_names[0], arg_string)




class EnglishPython(object):

    def __init__(self, f):
        self.func = f
        # Remove the None from the list
        self.code_obj = byteplay.Code.from_code(self.func.func_code)
        self.disassembly = self.code_obj.code
        self.english_translation = filter(lambda x: x[1] is not None, FakeRun(self.func).step_through_bytecode())

    def __str__(self):
        return '\n'.join(('\t'.join((str(l[0]), l[1])) for l in self.english_translation))

    def __repr__(self):
        return ' '.join((l[1] for l in self.english_translation))


class EnglishByte(object):

    translation = {'load': None, 'call': "{0}", 'store': "Store {0} as {1}.",\
                            'return': "Return {0}.", 'binary': "{1} {0} {2}"}
    operdict = {'add': '+', 'subtract': '-', 'multiply': '*', 'divide': '/'}

    def __init__(self, command, *byte_args):
        self.command = command
        self.byte_args = byte_args
        self.format_string = self.translation[self.command]
        self.formatted_string = self.format_string.format(byte_args)



    def full_english(self):
        if self.command == 'binary':
            result = ' '.join(('Compute', self.format_string.format(self.byte_args)))
        elif self.command == 'call':
            func_arg = self.byte_args[1:]
            if len(func_arg) == 0:
                suffix = 'no argument'
            elif len(func_arg) == 1:
                suffix = '{0} as argument'.format(func_arg)
            else:
                suffix = '{0} as arguments'.format(', '.join(str(func_arg)))
            result = 'Call {0} with {1}.'.format(self.formatted_string, suffix)
        elif self.command == 'return':
            pass
        return result

    def stack_english(self):
        pass


    def translate(self, command, arg_names):
        if not arg_names:
            return self.translation[command]
        elif command == 'BINARY_ADD' or command == 'BINARY_SUBTRACT' or command == 'BINARY_MULTIPLY' or command == 'BINARY_DIVIDE':
            return self.translation[command].format(arg_names)
        elif command == 'return':
            return self.translation[command].format(arg_names)
        elif command == 'store':
            return self.translation[command].format(arg_names[0], arg_names[1])
        elif command == 'call' and len(arg_names) == 1:
            return self.translation[command].format(arg_names[0], 'no argument.')
        elif command == 'call' and len(arg_names) == 2:
            return self.translation[command].format(arg_names[0], ' '.join([str(arg_names[1]),'as argument.']))
        elif command == 'call' and len(arg_names) > 2:
            arg_string = ' '.join([' and '.join(map(str, arg_names[1:])), 'as arguments.'])
            return self.translation[command].format(arg_names[0], arg_string)
