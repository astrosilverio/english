def f(x):
    if x == 1:
        pass
    return x

if __name__ == '__main__':
        from englishpython import *
        from subprocess import Popen

        print "\nFunction:"
        print "\ndef f(x)\n    if x == 1:\n    return x"
        a = EnglishPython(f)
        print "\nBytecode:"
        print a.disassembly
        print "Translation:\n"
        print(a)
        print "\n"
        #p = Popen(['say', a.__repr__()])


