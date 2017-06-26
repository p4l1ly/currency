#! /usr/bin/python

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
import cherrypy
from decimal import Decimal
import currency.app as currency
import json

app = Flask(__name__)

@app.route('/currency_converter')
def convert():
    amount = Decimal(request.args.get('amount', '1'))
    input_currency = request.args.get('input_currency', 'EUR')
    output_currency = request.args.get('output_currency', None)

    return app.response_class\
        ( response = currency.app(amount, input_currency, output_currency)
        , status   = 200
        , mimetype = 'application/json' )

if __name__ == '__main__':
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
