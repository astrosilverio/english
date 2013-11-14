import byteplay


class EnglishPython(object):

    def __init__(self, f):
        self.func = f
        self.stack = []
        self.code_obj = byteplay.Code.from_code(self.func.func_code)
        self.bytecode = self.code_obj.code
        self.english = []
        self.bytedict = {'load': self.load, 'call': self.call, 'store': self.store, 'return': self.ret}
        self.translation = {'load': None, 'call': "Call {0} with {1}", 'store': "Store {0} as {1}", 'return': "Return {0}"}

    def step_through_bytecode(self):
        for line in self.bytecode:
            command, args = line
            command = str(command)
            #pudb.set_trace()
            if command == 'SetLineno':
                line_num = args
                continue
            try:
                command = self.instruction_type(command)
                args_names = self.bytedict[command](args)
            except KeyError:
                print("We don't support {} yet.".format(command))
                break
            line_translation = self.translate(command, *args_names)
            self.english.append((line_num, line_translation))

    def call(self, num_args):
        f_and_args = self.stack[-(num_args+1):]
        self.stack = self.stack[:-(num_args+1)]
        stack_string = 'result of {}'.format(f_and_args[0])
        self.stack.append(stack_string)
        return f_and_args

    def load(self, thing):
        self.stack.append(thing)
        return []

    def store(self, thing):
        return self.stack.pop(), thing

    def ret(self, thing):
        return self.stack.pop()

    def instruction_type(self, com):
        if com.startswith("LOAD"):
            return "load"
        elif com.startswith("CALL"):
            return "call"
        elif com.startswith("STORE"):
            return "store"
        elif com.startswith("RETURN"):
            return "return"
        elif com.startswith("BINARY"):
            com[com.index('_'):]
        else:
            raise ValueError

    def translate(self, command, *arg_names):
        if not arg_names:
            return self.translation[command]
        elif len(arg_names) == 1:
            return self.translation[command].format(arg_names[0], 'no argument.')
        elif command == 'store':
            return self.translation[command].format(arg_names[0], arg_names[1])
        elif command == 'call' and len(arg_names) == 1:
            return self.translation[command].format(arg_names[0], ' '.join([str(arg_names[1]),'as argument.']))
        elif command == 'call' and len(arg_names) == 2:
            return self.translation[command].format(arg_names[0], ' '.join([str(arg_names[1]),'as argument.']))
        elif command == 'call' and len(arg_names) > 2:
            arg_string = ' '.join([' and '.join(map(str, arg_names[1:])), 'as arguments.'])
            return self.translation[command].format(arg_names[0], arg_string)

    def print_english(self):
        self.step_through_bytecode()
        for line in self.english:
            if line[1]:
                print(line)

if __name__ == '__main__':

    def foo(x):
        x = 2
        return x

    def crazy(x):
        x = add(age, substract(heigh, weight))
        return x

    english_foo = EnglishPython(foo)
    english_foo.print_english()

    english_crazy = EnglishPython(crazy)
    english_crazy.print_english()




