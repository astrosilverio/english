class EnglishByte(object):
    """
    Class for handling the different string formating operations
    of the english translation.
    """
    translation = {'load': "{0}", 'call': "result of call to {0}",
                   'store': "Store {0} as {1}.",'return': "Return {0}.",
                   'binary': "{1} {0} {2}", 'compare': "{1} {0} {2}", 'else': "Else:",
                   'pop': "If {0}, then:"}

    binary_operators = {'add': 'plus', 'subtract': 'minus', 'multiply': 'times',
                        'divide': 'divided by', 'power': 'raised to the power of',
                        'modulo': 'modulo', 'and': 'AND', 'or': 'OR', 'xor': 'XOR',
                        '==': "is equal to", '>': "is greater than",
                        '<': "is less than", '>=': "is greater or equal to",
                        '<=': "is less or equal to", '!=': "is not equal to",
                        'in': "is in"}

    short_english_only = {'load', 'compare'}

    def __init__(self, command, line_num, indents, *args):
        self.line_num = line_num
        self.indents = indents
        self.pre_formatted_string = self.translation[command]
        self.prefix = ""
        self.suffix = ""
        special_init = getattr(self, '{}_init'.format(command), self.default_init)
        special_init(args)

        if command != 'call' and command not in self.short_english_only:
            self.full = self._full_english()

    def default_init(self, args):
        self.short = self.pre_formatted_string.format(*args)
        
    def pop_init(self, args):
        jump_condition = args[1]
        self.short = self.pre_formatted_string.format(jump_condition)

    def return_init(self, args):
        return_value = args[1]
        self.short = self.pre_formatted_string.format(return_value)

    def binary_init(self, args):
        operation = self.binary_operators[args[0]]
        operand1 = args[1]
        operand2 = args[2]
        self.short = self.pre_formatted_string.format(operation, operand1,\
                                                      operand2)
        self.prefix = "Compute "

    def compare_init(self, args):
        comparison = self.binary_operators[args[0]]
        operand1 = args[1]
        operand2 = args[2]
        self.short = self.pre_formatted_string.format(comparison, operand1,\
                                                      operand2)

    def call_init(self, args):
        # args[0] is the number of arguments (not used here)
        func = args[1]
        self.short = self.pre_formatted_string.format(func)

        # dealing with the full english
        args_of_func= args[2:]
        if len(args_of_func) == 0:
                suffix = 'no argument'
        elif len(args_of_func) == 1:
            suffix = '{0} as argument'.format(*args_of_func)
        else:
            suffix = '{0} as arguments'.format(', '.join(map(str, args_of_func)))
        self.full = 'Call {0} with {1}.'.format(func, suffix)
        self.full = '\t'.join([self.line_num, self.full])

    def _full_english(self):
        result = ''.join([self.prefix, self.short, self.suffix])
        tabs = '\t'*(self.indents + 1)
        result = tabs.join([self.line_num, result])
        return result
