# -*- coding: utf-8 -*-

from .context import currency
import currency.fetcher as fetcher

import unittest
import requests

class UnitTestSuite(unittest.TestCase):
    """Testing the library."""

    def test_fixer(self):
        try:
            curr = fetcher.fetch_from_fixer('EUR', 'USD')
            assert(isinstance(curr, float))
        except requests.exceptions.RequestException:
            pass

if __name__ == '__main__':
    unittest.main()
