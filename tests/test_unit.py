# -*- coding: utf-8 -*-

from nose.tools import assert_raises, assert_equal, assert_is_instance
import unittest
from builtins import str

from decimal import Decimal

from .context import currency
import currency.fetcher as fetcher
import currency.symbol_dict as symbol_dict

class UnitTestSuite(unittest.TestCase):
    u"""Testing the library."""

    def test_fixer(self):
        curr = fetcher.from_fixer(u'EUR', u'CZK')
        print(u'fixer: 1 EUR = {} CZK'.format(curr))
        assert_is_instance(curr, Decimal)

    def test_cnb_czk(self):
        curr = fetcher.cnb_czk(u'EUR')
        print(u'cnb: 1 EUR = {} CZK'.format(curr))
        assert_is_instance(curr, Decimal)

    def test_cnb1(self):
        curr = fetcher.from_cnb(u'EUR', u'CZK')
        print(u'cnb: 1 EUR = {} CZK'.format(curr))
        assert_is_instance(curr, Decimal)

    def test_cnb2(self):
        curr = fetcher.from_cnb(u'CZK', u'EUR')
        print(u'cnb: 1 EUR = {} CZK'.format(Decimal(u'1') / curr))
        assert_is_instance(curr, Decimal)

    def test_cnb3(self):
        curr = fetcher.from_cnb(u'USD', u'DJF')
        print(u'cnb: 1 USD = {} DJF'.format(curr))
        assert_is_instance(curr, Decimal)

    def test_yahoo(self):
        curr = fetcher.from_yahoo(u'EUR', u'CZK')
        print(u'yahoo: 1 EUR = {} CZK'.format(curr))
        assert_is_instance(curr, Decimal)

    def test_fetcher_good(self):
        curr = fetcher.from_all(u'EUR', u'CZK')
        assert_is_instance(curr, Decimal)

    def test_fetcher_bad(self):
        assert_raises(fetcher.NotFound, fetcher.from_all, u'quux', u'bazz')

    def test_xe_symbol_dict(self):
        code = symbol_dict.from_xe(u'Lek')
        assert(code == u'ALL')

    def test_static_symbol_dict(self):
        code = symbol_dict.from_xe(u'₱')
        assert(code == u'CUP')

    def test_babel_symbol_dict(self):
        code = symbol_dict.from_babel(u'₹')
        assert(code == u'INR')

    def test_symbol_dict(self):
        assert_raises(KeyError, symbol_dict.from_all, u'foobar')

    def test_currency_fetch(self):
        input_code, output_code, curr = fetcher.currency(u'€', u'CZK')
        assert_is_instance(input_code, str)
        assert_is_instance(output_code, str)
        assert_is_instance(curr, Decimal)

    def test_currency_fetch_error(self):
        assert_raises(Exception, fetcher.currency, u'€', u'foobar')
        assert_raises(Exception, fetcher.currency, u'€', u'GQF')
        assert_raises(Exception, fetcher.currency, u'€', u'abcd')
        assert_raises(Exception, fetcher.currency, u'GQF', u'€')
        assert_raises(Exception, fetcher.currency, u'abcd', u'€')
        assert_raises(Exception, fetcher.currency, u'GQF', u'GQQ')
        assert_raises(Exception, fetcher.currency, u'abcd', u'GQQ')
        assert_raises(Exception, fetcher.currency, u'GQQ', u'abcd')
        assert_raises(Exception, fetcher.currency, u'efgh', u'abcd')

    def test_all_currencies_fetch(self):
        input_code, currs, failed = fetcher.all_currencies(u'€')
        input_code2, currs2, failed2 = fetcher.all_currencies(u'EUR')

        assert_equal(input_code, input_code2)
        assert_is_instance(input_code, str)
        assert_is_instance(currs, dict)
        assert_is_instance(failed, list)
        k = next(iter(currs))
        assert_is_instance(k, str)
        assert_is_instance(currs[k], Decimal)

        print(u'all_currencies OK count:', len(currs))
        print(u'all_currencies failed:', failed)

if __name__ == '__main__':
    unittest.main()
