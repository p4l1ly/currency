# -*- coding: utf-8 -*-

import unittest

from .context import scripts
import scripts.currency_converter as currency_converter

import sys
import json

class CliTestSuite(unittest.TestCase):
    """Testing command line interface."""

    def test_one(self):
        sys.argv = [ 'currency_converter.py'
                   , '--amount', '10'
                   , '--input_currency', 'EUR'
                   , '--output_currency', 'Kč' ]
        result = json.loads(currency_converter.main())
        assert('input' in result)
        assert('output' in result)
        assert('amount' in result['input'])
        assert('currency' in result['input'])
        assert('CZK' in result['output'])

    def test_all(self):
        sys.argv = [ 'currency_converter.py'
                   , '--amount', '10'
                   , '--input_currency', 'EUR' ]
        currency_converter.main()

        result = json.loads(currency_converter.main())
        assert('input' in result)
        assert('output' in result)
        assert('amount' in result['input'])
        assert('currency' in result['input'])
        assert('CZK' in result['output'])
        assert('USD' in result['output'])

    def test_fail(self):
        sys.argv = [ 'currency_converter.py'
                   , '--amount', '10'
                   , '--input_currency', 'QQQ'
                   , '--output_currency', 'QQQ' ]
        currency_converter.main()

        result = json.loads(currency_converter.main())
        assert('input' in result)
        assert('output' in result)
        assert('amount' in result['input'])
        assert('currency' in result['input'])
        assert(not result['output'].keys())

if __name__ == '__main__':
    unittest.main()
