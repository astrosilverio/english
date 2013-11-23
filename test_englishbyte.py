import englishbyte
import unittest

class TestEnglishByte(unittest.TestCase):

    fake_line_num = str(0)


    def test_return(self):

        return_1 = englishbyte.EnglishByte('return', self.fake_line_num, None, 1)
        self.assertEqual('Return 1', return_1.short)
        expected = '\t'.join((str(self.fake_line_num), 'Return 1.'))
        self.assertEqual(expected, return_1.full)

        return_x = englishbyte.EnglishByte('return', self.fake_line_num, None, 'a string')
        self.assertEqual('Return a string', return_x.short)
        expected = '\t'.join((str(self.fake_line_num), 'Return a string.'))
        self.assertEqual(expected, return_x.full)

        return_none = englishbyte.EnglishByte('return', self.fake_line_num, None, None)
        self.assertEqual('Return None', return_none.short)
        expected = '\t'.join((str(self.fake_line_num), 'Return None.'))
        self.assertEqual(expected, return_none.full)
        
    def test_load(self):
        
        load_1 = englishbyte.EnglishByte('load', self.fake_line_num, 1, ())
        self.assertEqual('1', load_1.short)
        
        load_x = englishbyte.EnglishByte('load', self.fake_line_num, 'x', ())
        self.assertEqual('x', load_x.short)
        
        load_none = englishbyte.EnglishByte('load', self.fake_line_num, None, ())
        self.assertEqual('None', load_none.short)
        
    def test_call(self):
    
        call_none = englishbyte.EnglishByte('call', self.fake_line_num, 1, 'foo')
        self.assertEqual('result of call to foo', call_none.short)
        expected = '\t'.join((str(self.fake_line_num), 'Call foo with no argument.'))
        self.assertEqual(expected, call_none.full)
        
        call_one = englishbyte.EnglishByte('call', self.fake_line_num, 2, 'foo', 'x')
        self.assertEqual('result of call to foo', call_one.short)
        expected = '\t'.join((str(self.fake_line_num), 'Call foo with x as argument.'))
        self.assertEqual(expected, call_one.full)
        
        call_two = englishbyte.EnglishByte('call', self.fake_line_num, 3, 'foo', 'x', 'y')
        self.assertEqual('result of call to foo', call_two.short)
        expected = '\t'.join((str(self.fake_line_num), 'Call foo with x, y as arguments.'))
        self.assertEqual(expected, call_two.full)
        
    def test_store(self):
    
        store_x_1 = englishbyte.EnglishByte('store', self.fake_line_num, 'x', '1')
        self.assertEqual('Store x as 1', store_x_1.short)
        expected = '\t'.join((str(self.fake_line_num), 'Store x as 1.'))
        self.assertEqual(expected, store_x_1.full)

        store_y_x = englishbyte.EnglishByte('store', self.fake_line_num, 'y', 'x')
        self.assertEqual('Store y as x', store_y_x.short)
        expected = '\t'.join((str(self.fake_line_num), 'Store y as x.'))
        self.assertEqual(expected, store_y_x.full)

        store_none = englishbyte.EnglishByte('store', self.fake_line_num, 'z', None)
        self.assertEqual('Store z as None', store_none.short)
        expected = '\t'.join((str(self.fake_line_num), 'Store z as None.'))
        self.assertEqual(expected, store_none.full)    
        
    def test_binary(self):
    
        binary_numbers = englishbyte.EnglishByte('binary', self.fake_line_num, 'power', '1', '2')
        self.assertEqual('1 raised to the power of 2', binary_numbers.short)
        expected = '\t'.join((str(self.fake_line_num), 'Compute 1 raised to the power of 2.'))
        self.assertEqual(expected, binary_numbers.full)
        
    def test_compare(self):
    
        compare_numbers = englishbyte.EnglishByte('compare', self.fake_line_num, '!=', '1', '2')
        self.assertEqual('1 is not equal to 2', compare_numbers.short)


if __name__ == '__main__':
    unittest.main(exit=False)
