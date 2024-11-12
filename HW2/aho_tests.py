import unittest
from aho import AhoCorasick

MCDC_FILE_NAME_LOGS = "search_mcdc_logs.csv"
MCDC_FILE_NAME_RES = "search_mcdc_res.csv"

class TestAhoCorasick(unittest.TestCase):
    def test_basic_functionality(self):
        patterns = ["he", "she", "his", "hers", "sajrivn", ""]
        ac = AhoCorasick(patterns, MCDC_FILE_NAME_LOGS)
        text = "ahishers"
        matches = ac.search(text)
        expected = [(1, "his"), (3, "she"), (4, "he"), (4, "hers")]
        self.assertEqual(matches, expected)

    def test_overlapping_patterns(self):
        patterns = ["a", "ab", "bca"]
        ac = AhoCorasick(patterns, MCDC_FILE_NAME_LOGS)
        text = "abcabcab"
        matches = ac.search(text)
        expected = [(0, "a"), (0, "ab"), (1, "bca"), (3, "a"), (3, "ab"), (4, "bca"), (6, "a"), (6, "ab")]
        self.assertEqual(matches, expected)

    def test_patterns_of_different_lengths(self):
        patterns = ["a", "abc", "abcd"]
        ac = AhoCorasick(patterns, MCDC_FILE_NAME_LOGS)
        text = "abcd"
        matches = ac.search(text)
        expected = [(0, "a"), (0, "abc"), (0, "abcd")]
        self.assertEqual(matches, expected)

    def test_no_matches(self):
        patterns = ["xyz", "uvw"]
        ac = AhoCorasick(patterns, MCDC_FILE_NAME_LOGS)
        text = "abcdefgh"
        matches = ac.search(text)
        expected = []
        self.assertEqual(matches, expected)

    def test_empty_text(self, ):
        patterns = ["abc", "def"]
        ac = AhoCorasick(patterns, MCDC_FILE_NAME_LOGS)
        text = ""
        matches = ac.search(text)
        expected = []
        self.assertEqual(matches, expected)

    def test_empty_patterns(self):
        patterns = []
        ac = AhoCorasick(patterns, MCDC_FILE_NAME_LOGS)
        text = "abcdefgh"
        matches = ac.search(text)
        expected = []
        self.assertEqual(matches, expected)

    def test_case_sensitivity(self):
        patterns = ["abc", "ABC"]
        ac = AhoCorasick(patterns, MCDC_FILE_NAME_LOGS)
        text = "abcABC"
        matches = ac.search(text)
        expected = [(0, "abc"), (3, "ABC")]
        self.assertEqual(matches, expected)

    def test_long_text(self):
        patterns = ["test", "long", "pattern"]
        ac = AhoCorasick(patterns, MCDC_FILE_NAME_LOGS)
        text = "this is a long string with multiple test patterns, including the word test and pattern."
        matches = ac.search(text)
        expected = [(10, "long"), (36, "test"), (41, "pattern"), (70, "test"), (79, "pattern")]
        self.assertEqual(matches, expected)

    def test_unicode_characters(self):
        patterns = ["你好", "世界", "hello"]
        ac = AhoCorasick(patterns, MCDC_FILE_NAME_LOGS)
        text = "你好世界hello"
        matches = ac.search(text)
        expected = [(0, "你好"), (2, "世界"), (4, "hello")]
        self.assertEqual(matches, expected)

if __name__ == "__main__":
    unittest.main()
