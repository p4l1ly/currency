# -*- coding: utf-8 -*-

import unittest

from .context import scripts
import scripts.currency_converter as currency_converter

import sys
import json

class CliTestSuite(unittest.TestCase):
    u"""Testing command line interface."""

    def test_one(self):
        sys.argv = [ u'currency_converter.py'
                   , u'--amount', u'10'
                   , u'--input_currency', u'EUR'
                   , u'--output_currency', u'Kč' ]
        result = json.loads(currency_converter.main())
        assert(u'input' in result)
        assert(u'output' in result)
        assert(u'amount' in result[u'input'])
        assert(u'currency' in result[u'input'])
        assert(u'CZK' in result[u'output'])

    def test_all(self):
        sys.argv = [ u'currency_converter.py'
                   , u'--amount', u'10'
                   , u'--input_currency', u'EUR' ]
        currency_converter.main()

        result = json.loads(currency_converter.main())
        assert(u'input' in result)
        assert(u'output' in result)
        assert(u'amount' in result[u'input'])
        assert(u'currency' in result[u'input'])
        assert(u'CZK' in result[u'output'])
        assert(u'USD' in result[u'output'])

    def test_fail(self):
        sys.argv = [ u'currency_converter.py'
                   , u'--amount', u'10'
                   , u'--input_currency', u'QQQ'
                   , u'--output_currency', u'QQQ' ]
        currency_converter.main()

        result = json.loads(currency_converter.main())
        assert(u'input' in result)
        assert(u'output' in result)
        assert(u'amount' in result[u'input'])
        assert(u'currency' in result[u'input'])
        assert(not result[u'output'].keys())

if __name__ == '__main__':
    unittest.main()
