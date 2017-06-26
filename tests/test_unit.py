# -*- coding: utf-8 -*-

from nose.tools import assert_raises, assert_equal
import unittest

from decimal import Decimal

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
        curr = fetcher.cnb_czk('EUR')
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

    def test_babel_symbol_dict(self):
        code = symbol_dict.from_babel('₹')
        assert(code == 'INR')

    def test_symbol_dict(self):
        assert_raises(KeyError, symbol_dict.from_all, 'foobar')

    def test_currency_fetch(self):
        input_code, output_code, curr = fetcher.currency('€', 'CZK')
        assert(isinstance(input_code, str))
        assert(isinstance(output_code, str))
        assert(isinstance(curr, Decimal))

    def test_currency_fetch_error(self):
        assert_raises(Exception, fetcher.currency, '€', 'foobar')
        assert_raises(Exception, fetcher.currency, '€', 'GQF')
        assert_raises(Exception, fetcher.currency, '€', 'abcd')
        assert_raises(Exception, fetcher.currency, 'GQF', '€')
        assert_raises(Exception, fetcher.currency, 'abcd', '€')
        assert_raises(Exception, fetcher.currency, 'GQF', 'GQQ')
        assert_raises(Exception, fetcher.currency, 'abcd', 'GQQ')
        assert_raises(Exception, fetcher.currency, 'GQQ', 'abcd')
        assert_raises(Exception, fetcher.currency, 'efgh', 'abcd')

    def test_all_currencies_fetch(self):
        input_code, currs, failed = fetcher.all_currencies('€')
        input_code2, currs2, failed2 = fetcher.all_currencies('EUR')

        assert_equal(input_code, input_code2)
        assert(isinstance(input_code, str))
        assert(isinstance(currs, dict))
        assert(isinstance(failed, list))
        k = next(iter(currs))
        assert(isinstance(k, str))
        assert(isinstance(currs[k], Decimal))

        print('all_currencies OK count:', len(currs))
        print('all_currencies failed:', failed)

if __name__ == '__main__':
    unittest.main()
