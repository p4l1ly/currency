# -*- coding: utf-8 -*-

u"""
This module implements the user interface of the currency converter application.
The interface implemented here is common for both the API and the CLI.
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

import simplejson as json
import currency.fetcher
from decimal import Decimal, ROUND_HALF_UP

def format_decimal(x):
    return x.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

def pretty_json(amount, input_currency, output):
    u"""
    Present the currency conversion result in the correct format

    :param amount: converted amount
    :type amount: :class:`decimal.Decimal`

    :param input_currency: input currency code
    :type input_currency: :class:`str`

    :param output: conversion result
    :type output: :class:`dict` < :class:`str` : :class:`decimal.Decimal` >

    :result: pretty formatted JSON string, as described in :doc:`README <index>`
    :rtype: :class:`str`
    """
    data = { u'input': {u'amount': amount, u'currency': input_currency}
           , u'output': output }

    data[u'input'][u'amount'] = format_decimal(data[u'input'][u'amount'])
    for k in data[u'output']:
        data[u'output'][k] = format_decimal(data[u'output'][k])

    return json.dumps(data, indent=4, sort_keys=True)

def app(amount, input_currency, output_currency=None):
    u"""
    Convert the **amount** in **input_currency** to **output_currency**. If
    **output_currency** is :class:`None` , convert to all known currencies.

    :param amount: converted amount
    :type amount: :class:`decimal.Decimal`

    :param input_currency: input currency code or symbol
    :type input_currency: :class:`str`

    :param output_currency: output currency code or symbol, or :class:`None` for
        output in all known currencies
    :type output_currency: :class:`str` or :class:`None`

    :result: pretty formatted JSON string, as described in :doc:`README <index>`
    :rtype: :class:`str`
    """
    if output_currency:
        input_code, output_code, curr = currency.fetcher.currency(
            input_currency, output_currency)

        output = {output_code: curr * amount} if curr is not None else {}

        return pretty_json(amount, input_code, output)

    else:
        input_code, currs, failed =\
            currency.fetcher.all_currencies(
                input_currency, output_currency)

        for code, curr in currs.items():
            currs[code] = curr * amount

        return pretty_json(amount, input_code, currs)
