import unittest

import util
from unittest_data_provider import data_provider


class test_util(unittest.TestCase):

    data_provider_median_bucket = lambda: (
        ([2], [101, 121, 131, 20, 24, 29, 123, 99]),
        ([3], [1, 0, 0, 1, 0, 1]),
        #([0, 5], [1, 0, 0, 0, 0, 1]),
        ([5], [1, 2, 3, 4, 5, 16]),
        ([4, 5], [1, 2, 3, 4, 5, 15]),
        ([4], [1, 2, 3, 4, 5, 14]),
        ([3, 4], [1, 2, 3, 4, 5, 5]),
    )

    @data_provider(data_provider_median_bucket)
    def test_median_bucket(self, expected, distribution):
        self.assertEqual(expected, util.median_bucket(distribution))

    data_provider_median_bucket_with_left_right = lambda: (
        ([2], [101, 121, 131, 20, 24, 29, 123, 99], 0, 0),
        ([2, 3], [101, 121, 131, 20, 24, 29, 123, 99], 100, 158),
        ([2], [101, 121, 131, 20, 24, 29, 123, 99], 100, 157),
        ([3], [101, 121, 131, 20, 24, 29, 123, 99], 100, 159),
    )
    @data_provider(data_provider_median_bucket_with_left_right)
    def test_median_bucket_with_left_right(self, expected, distribution, left, right):
        self.assertEqual(expected, util.median_bucket(distribution, left, right))
