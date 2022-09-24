import unittest

from sort_names import get_short_list
import filecmp


class TestGetShortList(unittest.TestCase):
    def test_get_short_list(self):
        self.assertFalse(
            filecmp.cmp("test.csv", "result.csv", shallow=False), "Files are same"
        )
