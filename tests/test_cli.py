# -*- coding: utf-8 -*-

import unittest

from .context import scripts
import scripts.currency_converter as currency_converter

import sys

class CliTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_one(self):
        sys.argv = [ 'currency_converter.py'
                   , '--amount', '10'
                   , '--input_currency', 'EUR'
                   , '--output_currency', 'Kč' ]
        currency_converter.main()

    def test_all(self):
        sys.argv = [ 'currency_converter.py'
                   , '--amount', '10'
                   , '--input_currency', 'EUR' ]
        currency_converter.main()

if __name__ == '__main__':
    unittest.main()
