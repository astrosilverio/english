def g(a, b, c):
        x = add(a, multiply(b, foo(c + 42)))
        return x

if __name__ == '__main__':
        from englishpython import *
        from subprocess import Popen

        print "\nFunction:"
        print "\ndef g(x)\n    x = add(a, multiply(b, foo(c + 42)))\n    return x"
        a = EnglishPython(g)
        print "\nBytecode:"
        print a.disassembly
        print "Translation:\n"
        print(a)
        print "\n"
        #p = Popen(['say', a.english_string()])