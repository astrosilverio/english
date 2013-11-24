import fakerun
import unittest
from englishbyte import EnglishByte
from collections import deque

class TestFakeRun(unittest.TestCase):

    def setUp(self):
    
        def foo(x):
            y = bar(4, 3+x)
            return x > y
               
        self.foo_fakerun = fakerun.FakeRun(foo, run=False, call_return=True)
        self.instructions_output = []
        for command, arg in self.foo_fakerun.instructions():
           self.instructions_output.append((command, arg))
           
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
        self.assertEqual('load', expected[0])
        self.assertEqual('bar', expected[2])
        self.assertEqual(deque([]), expected[3])
        
        expected = self.foo_fakerun.call_byte('load', 4)
        self.assertEqual(2, len(self.foo_fakerun._python_stack))
        self.assertEqual(0, len(self.foo_fakerun.english_stack))
        self.assertEqual('load', expected[0])
        self.assertEqual(4, expected[2])
        self.assertEqual(deque([]), expected[3])
        
        self.foo_fakerun.call_byte('load', 3)
        self.foo_fakerun.call_byte('load', 'x')
        
        expected = self.foo_fakerun.call_byte('binary', 'add')
        self.assertEqual(3, len(self.foo_fakerun._python_stack))
        self.assertEqual(1, len(self.foo_fakerun.english_stack))
        self.assertEqual('binary', expected[0])
        self.assertEqual('add', expected[2])
        self.assertEqual(deque(['3', 'x']), expected[3])
        
        expected = self.foo_fakerun.call_byte('call', 2)
        self.assertEqual(1, len(self.foo_fakerun._python_stack))
        self.assertEqual(2, len(self.foo_fakerun.english_stack))
        self.assertEqual('call', expected[0])
        self.assertEqual(2, expected[2])
        self.assertEqual(deque(['bar', '4', '3 plus x']), expected[3])
        
        expected = self.foo_fakerun.call_byte('store', 'y')
        self.assertEqual(0, len(self.foo_fakerun._python_stack))
        self.assertEqual(3, len(self.foo_fakerun.english_stack))
        self.assertEqual('store', expected[0])
        self.assertEqual('y', expected[2])
        self.assertEqual(deque(['result of call to bar']), expected[3])
        
        self.foo_fakerun.call_byte('load', 'x')
        self.foo_fakerun.call_byte('load', 'y')
        
        expected = self.foo_fakerun.call_byte('compare', '>')
        self.assertEqual(1, len(self.foo_fakerun._python_stack))
        self.assertEqual(3, len(self.foo_fakerun.english_stack))
        self.assertEqual('compare', expected[0])
        self.assertEqual('>', expected[2])
        self.assertEqual(deque(['x', 'y']), expected[3])
        
        expected = self.foo_fakerun.call_byte('return', None)
        self.assertEqual(0, len(self.foo_fakerun._python_stack))
        self.assertEqual(4, len(self.foo_fakerun.english_stack))
        self.assertEqual('return', expected[0])
        self.assertEqual(None, expected[2])
        self.assertEqual(deque(['x is greater than y']), expected[3])
        
    def test_run(self):
        self.foo_fakerun.english_stack = []
        self.foo_fakerun._python_stack = []
        self.foo_fakerun.run()
        
        self.assertEqual('11\tCompute 3 plus x.', self.foo_fakerun.english_stack[0].full)
        self.assertEqual('11\tCall bar with 4, 3 plus x as arguments.', self.foo_fakerun.english_stack[1].full)
        self.assertEqual('11\tStore y as result of call to bar.', self.foo_fakerun.english_stack[2].full)
        self.assertEqual('12\tReturn x is greater than y.', self.foo_fakerun.english_stack[3].full)
    
    
if __name__ == '__main__':
    unittest.main(exit=False)
    
        #load
#        def test_store():
#        def test_return():
#        def test_binary():
#        def test_compare():
#        def test_call():
