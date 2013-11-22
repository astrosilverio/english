import byteplay

def fact(n):
    if n <= 1:
        return 1
    else:
        return n * fact(n-1)
        
codeobj = byteplay.Code.from_code(fact.func_code)
disassembly = codeobj.code
loops=[]

tupledict = {'load': (0,1,0), 'store': (1,0,1), 'return': (1,0,1),
                 'binary': (2,1,1), 'compare': (2,1,0), 'call': (1, 1, 1),
                 'else': (0,0,1)}


def instructions():
    loops = []
    for line in disassembly:
        com_obj, byte_arg = line
        com = str(com_obj)
        if com == 'SetLineno':
            line_num = str(byte_arg)    
            print line_num      
            continue
        elif isinstance(com_obj, byteplay.Label):
            loops = loops[:loops.index(com_obj)]
            com = 'else_'
        elif com.startswith('POP_JUMP_IF'):
            loops.append(byte_arg)
            continue

        command_type = com[:com.find('_')].lower()
        if command_type not in tupledict:
            print("We don't support {} yet.".format(com))
            raise KeyError
        elif command_type == 'binary':
            argument = com[com.index('_') + 1:].lower()
        else:
            argument = byte_arg
        print command_type, argument



if __name__ == '__main__':
#     print disassembly
#     instructions()

        from englishpython import *
        from subprocess import Popen

        print "\nFunction:"
        print "\ndef fact(n)\n\tif x <= 1:\n\t\treturn 1\n\telse:\n\t\treturn n * fact(n-1)"
        a = EnglishPython(fact)
        print "\nBytecode:"
        print a.disassembly
        print "Translation:\n"
        print(a)
        print "\n"
        #p = Popen(['say', a.__repr__()])


