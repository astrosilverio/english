def h(butts):
        your_face = your_mom()
        return butts


if __name__ == '__main__':
        from englishpython import *
        from subprocess import Popen

        print "\nFunction:"
        print "\ndef h(x)\n    your_face = your_mom()\n    return butts"
        a = EnglishPython(h)
        print "\nBytecode:"
        print a.bytecode
        print "Translation:\n"
        a.print_english()
        print "\n"
        p = Popen(['say', a.english_string()])