import unittest

from crew_brief import sorting

class TestPaddedKeys(unittest.TestCase):

    def setUp(self):
        self.data = [
            {'a', 'b', 'c', 'd'},
            {'a', 'c', 'd'},
            {'a', 'd'},
            {'a', 'c', 'd'},
            set(),
            {'a', 'b'},
            {'a'},
            {'b'},
        ]

    def test_padded_keys_set(self):
        result = list(sorting.padded_keys(self.data))
        # Comes back in lists.
        expect = [
            ['a', 'b', 'c', 'd'],
            ['a', None, 'c', 'd'],
            ['a', None, None, 'd'],
            ['a', None, 'c', 'd'],
            [None, None, None, None],
            ['a', 'b', None, None],
            ['a', None, None, None],
            [None, 'b', None, None],
        ]
        self.assertEqual(result, expect)


class TestSplitDict(unittest.TestCase):

    def test_split_dict(self):
        data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        extracted, remaining = sorting.split_dict(data, 'cd')
        self.assertEqual(extracted, {'c': 3, 'd': 4})
        self.assertEqual(remaining, {'a': 1, 'b': 2})

    def test_split_nested(self):
        data = {'a': 1, 'b': 2, 'c': 3, 'd': {'z': 9, 'y': 8}}
        extracted, remaining = sorting.split_dict(data, 'cd')
        self.assertEqual(extracted, {'c': 3, 'd': {'z': 9, 'y': 8}})
        self.assertEqual(remaining, {'a': 1, 'b': 2})


class TestPadList(unittest.TestCase):

    def test_pad_list(self):
        list_ = [(1, 2), (1,), (1, 2, 3), (1, )]
        result = sorting.pad_list(list_)
        expect = [(1, 2, None), (1, None, None), (1, 2, 3), (1, None, None)]
        self.assertEqual(result, expect)


class TestJoinTables(unittest.TestCase):

    def test_join_tables(self):
        self.assertEqual(
            sorting.join_tables(
                [[0, 1, 2],
                 [3, 4],
                 [5, 6, 7, 8],
                 [9]],
                ['abc',
                 'de',
                 'fghi',
                 'j']
            ),
            [[0, 1, 2, None, 'a', 'b', 'c', None],
             [3, 4, None, None, 'd', 'e', None, None],
             [5, 6, 7, 8, 'f', 'g', 'h', 'i'],
             [9, None, None, None, 'j', None, None, None]],
        )


class TestDictSplit(unittest.TestCase):

    def setUp(self):
        self.splitter = sorting.DictSplit(['a'], ['b'], ['c'])

    def test_dict_split(self):
        result = self.splitter({'a': 1, 'b': 2, 'c': 3, 'd': 4})
        expect = {
            ('a',): {'a': 1},
            ('b',): {'b': 2},
            ('c',): {'c': 3},
            ('d',): {'d': 4},
        }
        self.assertEqual(result, expect)

    def test_dict_split_empty(self):
        result = self.splitter({})
        expect = {}
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
