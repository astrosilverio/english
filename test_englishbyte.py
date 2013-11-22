import englishbyte
import unittest

class TestEnglishByte(unittest.TestCase):

    fake_line_num = str(0)


    def test_return(self):

        return_1 = englishbyte.EnglishByte('return', self.fake_line_num, None, '1')
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




if __name__ == '__main__':
    unittest.main(exit=False)
