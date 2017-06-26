# -*- coding: utf-8 -*-

u"""
Currency converter API server. For :ref:`request description <params>` and
:ref:`examples of use <api>`, see :doc:`README <index>`.
"""

__author__     = u"Pavol Vargovčík"
__copyright__  = u"Copyright (c) 2017 Pavol Vargovčík"
__credits__    = [u"Pavol Vargovčík"]
__license__    = u"MIT"
__version__    = u"0.1.0"
__maintainer__ = u"Pavol Vargovčík"
__email__      = u"pavol.vargovcik@gmail.com"
__status__     = u"Development"
__docformat__  = u'reStructuredText'

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
import cherrypy
from decimal import Decimal
import currency.app as currency
import json

def init_app():
    app = Flask(__name__)

    @app.route(u'/currency_converter')
    def convert():
        u"""
        Convert **amount** (default: 1) money in **input_currency** to the
        equivalent amount in **output_currency**. If **output_currency**
        parameter is not specified, convert the amount into all known
        currencies. If the conversion is unsuccessful (the currencies are not
        known), the `u"output"` object in the JSON response is empty.

        **Example request**:

        .. sourcecode:: http

           GET /currency_converter?currency_converter?amount=10&input_currency=€&output_currency=CZK HTTP/1.1

        **Example response**:

        .. sourcecode:: http

           HTTP/1.1 200 OK
           Content-Type: application/json

        .. sourcecode:: json

           {
               "input": {
                   "amount": 1,
                   "currency": "EUR"
               },
               "output": {
                   "CZK": 26.2420
               }
           }

        :query amount: converted amount (decimal number)
        :query input_currency: input currency code or symbol
        :query output_currency: input currency code or symbol
        :resheader Content-Type: application/json
        :statuscode 200: no error
        """

        amount = Decimal(request.args.get(u'amount', u'1'))
        input_currency = request.args.get(u'input_currency', u'EUR')
        output_currency = request.args.get(u'output_currency', None)

        return app.response_class\
            ( response = currency.app(amount, input_currency, output_currency)
            , status   = 200
            , mimetype = u'application/json' )

    return app

def main():
    app = init_app()

    handler = RotatingFileHandler(u'/var/log/currency.log',
        u'a', 20*1024*1024, 1)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    cherrypy.tree.graft(app, u'/')

    # Set the configuration of the web server
    cherrypy.config.update(
        { u'engine.autoreload.on': False
        , u'log.screen': True
        , u'server.socket_port': 80
        , u'server.socket_host': u'0.0.0.0' })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
