# -*- coding: utf-8 -*-

from .context import currency
import currency.fetcher as fetcher

import unittest
import requests

class UnitTestSuite(unittest.TestCase):
    """Testing the library."""

    def test_fixer(self):
        curr = fetcher.from_fixer('EUR', 'CZK')
        print('fixer: 1 EUR = {} CZK'.format(curr))
        assert(isinstance(curr, float))

    def test_cnb_czk(self):
        curr = fetcher.cnb_czk_currency('EUR')
        print('cnb: 1 EUR = {} CZK'.format(curr))
        assert(isinstance(curr, float))

    def test_cnb1(self):
        curr = fetcher.from_cnb('EUR', 'CZK')
        print('cnb: 1 EUR = {} CZK'.format(curr))
        assert(isinstance(curr, float))

    def test_cnb2(self):
        curr = fetcher.from_cnb('CZK', 'EUR')
        print('cnb: 1 EUR = {} CZK'.format(1 / curr))
        assert(isinstance(curr, float))

    def test_cnb3(self):
        curr = fetcher.from_cnb('USD', 'DJF')
        print('cnb: 1 USD = {} DJF'.format(curr))
        assert(isinstance(curr, float))

if __name__ == '__main__':
    unittest.main()
