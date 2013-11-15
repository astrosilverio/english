import byteplay
import pdb


class EnglishPython(object):

    def __init__(self, f):
        self.func = f
        self.stack = []
        self.code_obj = byteplay.Code.from_code(self.func.func_code)
        self.bytecode = self.code_obj.code
        self.english = []
        self.bytedict = {'load': self.load, 'call': self.call, 'store': self.store, 'return': self.ret, 'BINARY_ADD': lambda x: self.binary('add', x), 'BINARY_MULTIPLY': lambda x: self.binary('multiply',x)}
        self.translation = {'load': None, 'call': "Call {0} with {1}", 'store': "Store {0} as {1}.", 'return': "Return {0}.", 'BINARY_ADD': "Compute {0}.", 'BINARY_MULTIPLY': "Compute {0}."}
        self.operdict = {'add': '+', 'subtract': '-', 'multiply': '*', 'divide': '/'}


    def step_through_bytecode(self):
        for line in self.bytecode:
            command, args = line
            command = str(command)
            if command == 'SetLineno':
                line_num = args
            else:
                try:
                    command = self.instruction_type(command)
                    args_names = self.bytedict[command](args)
#                                       print self.stack
                except KeyError:
                    print "We don't support {} yet.".format(command)
                    continue
                line_translation = self.translate(command, args_names)
                self.english.append((line_num, line_translation))

    def call(self,num_args):
        f_and_args = self.stack[-(num_args+1):]
        self.stack = self.stack[:-(num_args+1)]
        stack_string = 'result of call to {}'.format(f_and_args[0])
        self.stack.append(stack_string)
        return f_and_args

    def load(self,thing):
        self.stack.append(thing)
        return []

    def store(self,thing):
        return [self.stack.pop(), thing]

    def ret(self,thing):
        return self.stack.pop()

    def binary(self, thing, otherthing):
        operand1 = self.stack.pop()
        operand2 = self.stack.pop()
        operation = self.operdict[thing]
        stack_string = 'result of {0} {1} {2}'.format(operand1, operation, operand2)
        self.stack.append(stack_string)
        return '{0} {1} {2}'.format(operand1, operation, operand2)

    def instruction_type(self,com):
        if com.startswith("LOAD"):
            return "load"
        elif com.startswith("CALL"):
            return "call"
        elif com.startswith("STORE"):
            return "store"
        elif com.startswith("RETURN"):
            return "return"
        else:
            return com

    def translate(self,command, arg_names):
#               print command, arg_names
#               pdb.set_trace()
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

    def print_english(self):
        self.step_through_bytecode()
        for line in self.english:
            if line[1]:
                print line

def foo(x):
    x = x * x
    return x + 1

def g(x):
    y = add(x, 60)
    return y

def h():
    z = hello_world()
    return z

if __name__ == '__main__':
    a = EnglishPython(foo)
    a.print_english()

    b = EnglishPython(g)
    b.print_english()

    c = EnglishPython(h)
    c.print_english()
