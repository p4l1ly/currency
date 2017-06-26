import simplejson as json
import currency.fetcher

def pretty_json(amount, input_currency, output):
    """
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
    data = { 'input': {'amount': amount, 'currency': input_currency}
           , 'output': output }
    return json.dumps(data, indent=4, sort_keys=True)

def app(amount, input_currency, output_currency=None):
    """
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
        try:
            input_code, output_code, curr = currency.fetcher.currency(
                input_currency, output_currency)
            output = {output_code: curr * amount}

        except IndexError:
            input_code = input_currency
            output = {}

        return pretty_json(amount, input_code, output)

    else:
        input_code, currs, failed =\
            currency.fetcher.all_currencies(
                input_currency, output_currency)

        for code, curr in currs.items():
            currs[code] = curr * amount

        return pretty_json(amount, input_code, currs)
