
class EnglishByte(object):
    """
    Class for handling the different string formating operations
    of the english translation.
    """
    translation = {'load': "{0}", 'call': "result of call to {0}", 'store': "Store {0} as {1}",
                   'return': "Return {0}", 'binary': "{1} {0} {2}", 'compare': "{1} {0} {2}"}

    binary_operators = {'add': 'plus', 'subtract': 'minus', 'multiply': 'times', 'divide': 'divided by',
                        'power': 'raised to the power of', 'modulo': 'modulo', 'and': 'AND', 'or': 'OR',
                        'xor': 'XOR', '==': "is equal to", '>': "is greater than", '<': "is less than",
                        '>=': "is greater or equal to", '<=': "is less or equal to",
                        '!=': "is not equal to", 'in': "is in"}

    short_english_only = {'load', 'compare'}

    def __init__(self, command, *byte_args):
        self.arg_init = {'binary': self.binary_init, 'compare': self.compare_init, 'return': self.return_init,
                         'call': self.call_init}
        self.pre_formatted_string = self.translation[command]
        self.prefix = ""
        self.suffix = "."
        self.arg_init.get(command, self.default_init)(byte_args)

        if command != 'call' and command not in self.short_english_only:
            self.full = self._full_english()

    def default_init(self, byte_args):
        self.short = self.pre_formatted_string.format(*byte_args)

    def return_init(self, byte_args):
        return_value = byte_args[1]
        self.short = self.pre_formatted_string.format(return_value)

    def binary_init(self, byte_args):
        operation = self.binary_operators[byte_args[0]]
        operand1 = byte_args[1]
        operand2 = byte_args[2]
        self.short = self.pre_formatted_string.format(operation, operand1, operand2)

        self.prefix = "Compute "

    def compare_init(self, byte_args):
        comparison = self.binary_operators[byte_args[0]]
        operand1 = byte_args[1]
        operand2 = byte_args[2]
        self.short = self.pre_formatted_string.format(comparison, operand1, operand2)

    def call_init(self, byte_args):
        # byte_args[0] is the number of arguments (not used here)
        func = byte_args[1]
        self.short = self.pre_formatted_string.format(func)

        # dealing with the full english
        args_of_func= byte_args[2:]
        if len(args_of_func) == 0:
                suffix = 'no argument'
        elif len(args_of_func) == 1:
            suffix = '{0} as argument'.format(*args_of_func)
        else:
            suffix = '{0} as arguments'.format(', '.join(map(str, args_of_func)))
        self.full = 'Call {0} with {1}.'.format(func, suffix)

    def _full_english(self):
        result = ''.join([self.prefix, self.short, self.suffix])
        return result
