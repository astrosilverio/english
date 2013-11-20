
class EnglishByte(object):
    """
    Class for handling the different string formating operations
    of the english translation.
    """
    translation = {'load': "{0}", 'call': "{0}", 'store': "Store {0} as {1}.",
                   'return': "Return {0}.", 'binary': "{1} {0} {2}"}

    operdict = {'add': 'plus', 'subtract': 'minus', 'multiply': 'times', 'divide': 'divided by',
                'power': 'raised to the power of', 'modulo': 'modulo', 'and': 'AND', 'or': 'OR',
                'xor': 'XOR'}

    full_english_only = {'store', 'return'}

    def __init__(self, command, *byte_args):
        self.command = command
        self.byte_args = byte_args
        if self.command == 'binary':
            operation = self.operdict[self.byte_args[0]]
            operand1 = self.byte_args[1]
            operand2 = self.byte_args[2]
            self.byte_args = (operation, operand1, operand2)
        self.formatted_string = self.translation[self.command].format(*self.byte_args)
        self.short = self.short_english()
        self.full = self.full_english()

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
                suffix = '{0} as arguments'.format(', '.join(map(str, func_arg)))
            result = 'Call {0} with {1}.'.format(self.formatted_string, suffix)
        elif self.command in self.full_english_only:
            result = self.formatted_string
        else:
            result = None
        return result

    def short_english(self):
        if self.command in self.full_english_only:
            result = None
        else:
            result = self.formatted_string
        return result
