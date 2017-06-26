#! /usr/bin/python

"""
Currency converter API server. For :ref:`request description <params>` and
:ref:`examples of use <api>`, see :doc:`README <index>`.
"""

__author__     = "Pavol Vargovčík"
__copyright__  = "Copyright (c) 2017 Pavol Vargovčík"
__credits__    = ["Pavol Vargovčík"]
__license__    = "MIT"
__version__    = "0.1.0"
__maintainer__ = "Pavol Vargovčík"
__email__      = "pavol.vargovcik@gmail.com"
__status__     = "Development"
__docformat__  = 'reStructuredText'

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
import cherrypy
from decimal import Decimal
import currency.app as currency
import json

def init_app():
    app = Flask(__name__)

    @app.route('/currency_converter')
    def convert():
        """
        Convert **amount** (default: 1) money in **input_currency** to the
        equivalent amount in **output_currency**. If **output_currency**
        parameter is not specified, convert the amount into all known
        currencies. If the conversion is unsuccessful (the currencies are not
        known), the `"output"` object in the JSON response is empty.

        **Example request**:

        .. sourcecode:: http

           GET /currency_converter?currency_converter?amount=10&input_currency=€&output_currency=CZK HTTP/1.1

        **Example response**:

        .. sourcecode:: http

           HTTP/1.1 200 OK
           Content-Type: application/json

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

        amount = Decimal(request.args.get('amount', '1'))
        input_currency = request.args.get('input_currency', 'EUR')
        output_currency = request.args.get('output_currency', None)

        return app.response_class\
            ( response = currency.app(amount, input_currency, output_currency)
            , status   = 200
            , mimetype = 'application/json' )

    return app

if __name__ == '__main__':
    app = init_app()

    handler = RotatingFileHandler('/var/log/currency.log',
        'a', 20*1024*1024, 1)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server
    cherrypy.config.update(
        { 'engine.autoreload.on': False
        , 'log.screen': True
        , 'server.socket_port': 80
        , 'server.socket_host': '0.0.0.0' })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
