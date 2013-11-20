def f(x):
    return 1


if __name__ == '__main__':
        from englishpython import *
        from subprocess import Popen

        print "\nFunction:"
        print "\ndef f(x)\n    x = x * x\n    return x + 1"
        a = EnglishPython(f)
        print "\nBytecode:"
        print a.disassembly
        print "Translation:\n"
        print(a)
        print "\n"
        #p = Popen(['say', a.__repr__()])


