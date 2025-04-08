import unittest

from file_zipper.parse import collapse_dict

class TestParseCollapse(unittest.TestCase):

    def test_no_collapse(self):
        self.assertEqual(collapse_dict({'a': 1, 'b': 2}), {'a': 1, 'b': 2})

        result = collapse_dict({'a1': 1, 'a2': 2, 'b': 3})
        expect = {'a1': 1, 'a2': 2, 'b': 3}
        self.assertEqual(result, expect)

    def test_collapse_similar_keys_and_same_value(self):
        result = collapse_dict({'a1': 1, 'a2': 1, 'a3': 1, 'b': 2})
        expect = {'a': 1, 'b': 2}
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
