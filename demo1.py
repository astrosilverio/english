import byteplay

def fact(n):
    if n <= 1:
        return 1
    else:
        return n * fact(n-1)
        
if __name__ == '__main__':

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


