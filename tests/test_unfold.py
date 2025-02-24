import unittest

from crew_brief.unfold import unfold_dict

class TestUnfoldDict(unittest.TestCase):

    def test_unfold_dict_flat_dict(self):
        output = list(unfold_dict(dict(
            a = 1,
            b = 2,
            c = None,
        )))
        expect = [
            ('a', 'b', 'c'),
            (1, 2, None),
        ]
        self.assertEqual(output, expect)

    def test_unfold_dict_empty_nested(self):
        output = list(unfold_dict(dict(
            a = 1,
            b = 2,
            c = dict(),
        )))
        expect = [
            ('a', 'b', 'c'),
            (1, 2, {}),
        ]
        self.assertEqual(output, expect)

    @unittest.skip('Skip for development.')
    def test_unfold_very_deep(self):
        data = {
            'a': 1,
            'b': 2,
            'c': {
                'x': 'success',
                'y': 'procedure',
                'z': {
                    'f': 3.141,
                    'g': 2.718,
                    'h': 0,
                },
            },
        }
        expect = [
            ('a',  'b',  'c'),
            (None, None, 'x',       'y',         'z'),
            (None, None, None,      None,        'f',   'g',   'h'),
            (1,    2,    'success', 'procedure', 3.141, 2.718, 0),
        ]
        output = list(unfold_dict(data))
        self.assertEqual(output, expect)

    def test_unfold_dict_nested_one_level(self):
        output = list(unfold_dict(dict(
            a = 1,
            b = 2,
            c = dict(
                k1 = 'z',
            ),
        )))
        expect = [
            ('a', 'b', 'c.k1'),
            (1, 2, 'z'),
        ]
        self.assertEqual(output, expect)

    def test_unfold_dict_deeply_nested(self):
        output = list(unfold_dict(dict(
            a = 1,
            b = 2,
            c = dict(
                k1 = dict(
                    kk1 = 3.141,
                    kk2 = 1.234,
                ),
                k2 = 'z',
            ),
        )))
        expect = [
            ('a', 'b', 'c.k2', 'c.k1.kk1', 'c.k1.kk2'),
            (1, 2, 'z', 3.141, 1.234),
        ]
        self.assertEqual(output, expect)


if __name__ == '__main__':
    unittest.main()
