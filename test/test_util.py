import unittest
import datetime

import util

class test_util(unittest.TestCase):
    def test_median_bucket(self):
        distribution = [101, 121, 131, 20, 24, 29, 123, 99]
        self.assertEqual(2, util.median_bucket(distribution))
