import englishbyte
import unittest

class TestEnglishByte(unittest.TestCase):

    fake_line_num = 0


    def test_return(self):

        return_1 = englishbyte.EnglishByte('return', self.fake_line_num, None, '1')
        self.assertEqual('1', return_1.short)
        expected = '\t'.join((str(self.fake_line_num), 'Return 1.'))
        self.assertEqual(expected, return_1.full)

        return_x = englishbyte.EnglishByte('return', self.fake_line_num, None, 'a string')
        self.assertEqual('a string', return_x.short)
        expected = '\t'.join((str(self.fake_line_num), 'Retun a string.'))
        self.assertEqual(expected, return_x.full)

        return_none = englishbyte.EnglishByte('return', self.fake_line_num, None, None)
        self.assertEqual('None', return_none.short)
        expected = '\t'.join((str(self.fake_line_num), 'Retun None.'))
        self.assertEqual(expected, return_none.full)




if __name__ == '__main__':
    unittest.main(exit=False)
