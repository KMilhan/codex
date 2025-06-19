import unittest

from seek_sequence import seek_sequence


def to_vec(strings):
    return [s for s in strings]


class SeekSequenceTests(unittest.TestCase):
    def test_exact_match_finds_sequence(self):
        lines = to_vec(["foo", "bar", "baz"])
        pattern = to_vec(["bar", "baz"])
        self.assertEqual(seek_sequence(lines, pattern, 0, False), 1)

    def test_rstrip_match_ignores_trailing_whitespace(self):
        lines = to_vec(["foo   ", "bar\t\t"])
        pattern = to_vec(["foo", "bar"])
        self.assertEqual(seek_sequence(lines, pattern, 0, False), 0)

    def test_trim_match_ignores_leading_and_trailing_whitespace(self):
        lines = to_vec(["    foo   ", "   bar\t"])
        pattern = to_vec(["foo", "bar"])
        self.assertEqual(seek_sequence(lines, pattern, 0, False), 0)

    def test_pattern_longer_than_input_returns_none(self):
        lines = to_vec(["just one line"])
        pattern = to_vec(["too", "many", "lines"])
        self.assertIsNone(seek_sequence(lines, pattern, 0, False))


if __name__ == "__main__":
    unittest.main()

