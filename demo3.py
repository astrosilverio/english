def h(butts):
        your_face = your_mom()
        return butts


if __name__ == '__main__':
        from englishpython import *
        from subprocess import Popen

        print "\n Python Code:"
        print "\ndef h(x)\n\tyour_face = your_mom()\n\treturn butts"
        a = EnglishPython(h)
        print "\nBytecode:"
        print a.disassembly
        print "Translation:\n"
        print(a)
        print "\n"
        p = Popen(['say', a.__str__()])
