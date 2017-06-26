# -*- coding: utf-8 -*-

import unittest
import scripts.currency_converter_server as server

import json

class ApiTestSuite(unittest.TestCase):
    """Currency converter server testing."""

    def setUp(self):
        app = server.init_app()
        app.testing = True
        self.app = app.test_client()

    def test_one(self):
        response = self.app.get("/currency_converter"
                                "?amount=1"
                                "&input_currency=EUR"
                                "&output_currency=CZK")
        result = json.loads(next(response.response))
        assert('input' in result)
        assert('output' in result)
        assert('amount' in result['input'])
        assert('currency' in result['input'])
        assert('CZK' in result['output'])
        assert(isinstance(result['output']['CZK'], float))

    def test_all(self):
        response = self.app.get("/currency_converter"
                                "?amount=1"
                                "&input_currency=EUR")
        result = json.loads(next(response.response))
        assert('input' in result)
        assert('output' in result)
        assert('amount' in result['input'])
        assert('currency' in result['input'])
        assert('CZK' in result['output'])
        assert('USD' in result['output'])
        assert(isinstance(result['output']['CZK'], float))

if __name__ == '__main__':
    unittest.main()
