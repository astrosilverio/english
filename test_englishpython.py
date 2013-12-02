from englishpython import EnglishPython
import unittest

def f(x):
    if x:
        return x
    else:
        return 0

class TestEnglishPython(unittest.TestCase):
    def test_create_num_tabs(self):
        a = EnglishPython(f)
        a.create_num_tabs()
        expected = {2: 0, 3: 1, 4:0, 5:1}
        self.assertEqual(expected, a.num_tabs)


if __name__ == '__main__':
    unittest.main(exit=False)


