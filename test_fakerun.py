import fakerun
import unittest
from englishbyte import EnglishByte

class TestFakeRun(unittest.TestCase):

    def setUp(self):
    
        def foo(x):
            y = bar(4, 3+x)
            return x > y
               
        self.foo_fakerun = fakerun.FakeRun(foo, run=False, call_return=True)
        self.instructions_output = []
        for command, arg in self.foo_fakerun.instructions():
           self.instructions_output.append((command, arg))
           
        def call_byte_return(command, arg):
            if command == 'call': # num_pop should be arg + 1
                num_pop, num_stack, num_eng = (arg + 1, 1, 1)
            else:
                num_pop, num_stack, num_eng = self.foo_fakerun.tupledict[command]
            pops = deque()
            for _ in range(num_pop):
                pops.appendleft(self.foo_fakerun._python_stack.pop().short)
            byte_string = EnglishByte(command, self.line_num, arg, *pops) 
            if num_stack:
                self.foo_fakerun._python_stack.append(byte_string)
            if num_eng:
                self.english_stack.append(byte_string)           
            return command, self.foo_fakerun.line_num, arg, pops
            
        self.call_byte_return(command, arg) = call_byte_return

    def test_instructions(self):
               
        self.assertEqual(('load','bar'), self.instructions_output[0])
        self.assertEqual(('binary','add'), self.instructions_output[4])
        self.assertEqual(('call', 2), self.instructions_output[5])
        self.assertEqual(('store', 'y'), self.instructions_output[6])
        self.assertEqual(('compare', '>'), self.instructions_output[9])
        self.assertEqual(('return', None), self.instructions_output[10])
        
    def test_call_byte(self):
    
        expected = self.foo_fakerun.call_byte('load','bar')
        self.assertEqual(1, len(self.foo_fakerun._python_stack))
        self.assertEqual(0, len(self.foo_fakerun.english_stack))        
        
        self.foo_fakerun.call_byte('load', 4)
        self.assertEqual(2, len(self.foo_fakerun._python_stack))
        self.assertEqual(0, len(self.foo_fakerun.english_stack))
        
        self.foo_fakerun.call_byte('load', 3)
        self.foo_fakerun.call_byte('load', 'x')
        
        self.foo_fakerun.call_byte('binary', 'add')
        self.assertEqual(3, len(self.foo_fakerun._python_stack))
        self.assertEqual(1, len(self.foo_fakerun.english_stack))
        
        self.foo_fakerun.call_byte('call', 2)
        self.assertEqual(1, len(self.foo_fakerun._python_stack))
        self.assertEqual(2, len(self.foo_fakerun.english_stack))
        
        self.foo_fakerun.call_byte('store', 'y')
        self.assertEqual(0, len(self.foo_fakerun._python_stack))
        self.assertEqual(3, len(self.foo_fakerun.english_stack))
        
        self.foo_fakerun.call_byte('load', 'x')
        self.foo_fakerun.call_byte('load', 'y')
        
        self.foo_fakerun.call_byte('compare', '>')
        self.assertEqual(1, len(self.foo_fakerun._python_stack))
        self.assertEqual(3, len(self.foo_fakerun.english_stack))
        
        self.foo_fakerun.call_byte('return', None)
        self.assertEqual(0, len(self.foo_fakerun._python_stack))
        self.assertEqual(4, len(self.foo_fakerun.english_stack))
    
    
    
if __name__ == '__main__':
    unittest.main(exit=False)
    
        #load
#        def test_store():
#        def test_return():
#        def test_binary():
#        def test_compare():
#        def test_call():
