def f(x):
	x = x * x
	return x + 1


if __name__ == '__main__':
	import english
	from subprocess import Popen
	
	print "\nFunction:"
	print "\ndef f(x)\n    x = x * x\n    return x + 1"
	a = english.EnglishPython(f)
	print "\nBytecode:"
	print a.bytecode
	print "Translation:\n"
	print(a)
	print "\n"
	p = Popen(['say', a.__repr__()])
	
	
