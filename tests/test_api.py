# -*- coding: utf-8 -*-

from nose.tools import assert_is_instance
import unittest
import currency.api as server

import json

class ApiTestSuite(unittest.TestCase):
    u"""Currency converter server testing."""

    def setUp(self):
        app = server.init_app()
        app.testing = True
        self.app = app.test_client()

    def test_one(self):
        response = self.app.get(u'/currency_converter'
                                u'?amount=1'
                                u'&input_currency=EUR'
                                u'&output_currency=CZK')
        result = json.loads(next(response.response))
        assert(u'input' in result)
        assert(u'output' in result)
        assert(u'amount' in result[u'input'])
        assert(u'currency' in result[u'input'])
        assert(u'CZK' in result[u'output'])
        assert_is_instance(result[u'output'][u'CZK'], float)

    def test_all(self):
        response = self.app.get(u'/currency_converter'
                                u'?amount=1'
                                u'&input_currency=EUR')
        result = json.loads(next(response.response))
        assert(u'input' in result)
        assert(u'output' in result)
        assert(u'amount' in result[u'input'])
        assert(u'currency' in result[u'input'])
        assert(u'CZK' in result[u'output'])
        assert(u'USD' in result[u'output'])
        assert_is_instance(result[u'output'][u'CZK'], float)

if __name__ == '__main__':
    unittest.main()
