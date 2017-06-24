# -*- coding: utf-8 -*-

from nose.tools import assert_raises
import unittest

from decimal import Decimal
import requests

from .context import currency
import currency.fetcher as fetcher
import currency.symbol_dict as symbol_dict

class UnitTestSuite(unittest.TestCase):
    """Testing the library."""

    def test_fixer(self):
        curr = fetcher.from_fixer('EUR', 'CZK')
        print('fixer: 1 EUR = {} CZK'.format(curr))
        assert(isinstance(curr, Decimal))

    def test_cnb_czk(self):
        curr = fetcher.cnb_czk_currency('EUR')
        print('cnb: 1 EUR = {} CZK'.format(curr))
        assert(isinstance(curr, Decimal))

    def test_cnb1(self):
        curr = fetcher.from_cnb('EUR', 'CZK')
        print('cnb: 1 EUR = {} CZK'.format(curr))
        assert(isinstance(curr, Decimal))

    def test_cnb2(self):
        curr = fetcher.from_cnb('CZK', 'EUR')
        print('cnb: 1 EUR = {} CZK'.format(Decimal('1') / curr))
        assert(isinstance(curr, Decimal))

    def test_cnb3(self):
        curr = fetcher.from_cnb('USD', 'DJF')
        print('cnb: 1 USD = {} DJF'.format(curr))
        assert(isinstance(curr, Decimal))

    def test_yahoo(self):
        curr = fetcher.from_yahoo('EUR', 'CZK')
        print('yahoo: 1 EUR = {} CZK'.format(curr))
        assert(isinstance(curr, Decimal))

    def test_fetcher_good(self):
        curr = fetcher.from_all('EUR', 'CZK')
        assert(isinstance(curr, Decimal))

    def test_fetcher_bad(self):
        assert_raises(fetcher.NotFound, fetcher.from_all, 'quux', 'bazz')

    def test_xe_symbol_dict(self):
        code = symbol_dict.from_xe('Lek')
        assert(code == 'ALL')

    def test_static_symbol_dict(self):
        code = symbol_dict.from_xe('₱')
        assert(code == 'CUP')

    def test_symbol_dict(self):
        assert_raises(KeyError, symbol_dict.from_all, 'foobar')

if __name__ == '__main__':
    unittest.main()
