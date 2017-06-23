"""
TODO
"""

import re
from enum import Enum
from .helpers import get

class NotFound(Exception): pass

def from_all(input_code, output_code):
    """
    Try all implemented techniques to get as good currency as possible. The
    first pick is Yahoo. If it fails, fixer.io and cnb.cz are used as fallbacks.

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: :class:`str`

    :returns: the currency
    :rtype: :class:`float`
    """

    for fetch in [from_yahoo, from_fixer, from_cnb]:
        try:
            return fetch(input_code, output_code)
        except Exception as e:
            err = e

    raise err

def from_fixer(input_code, output_code):
    """
    Fetch currency from JSON API at https://api.fixer.io

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: :class:`str`

    :returns: the currency
    :rtype: :class:`float`
    """

    req = get('https://api.fixer.io/latest?base={}&symbols={}'.format(
        input_code, output_code))

    return req.json()['rates'][output_code]

def from_cnb(input_code, output_code):
    """
    Fetch currency from Czech National Bank. The currencies are not very fresh
    and they are rounded to three decimal places. But there are more of them
    than on fixer.

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: :class:`str`

    :returns: the currency
    :rtype: :class:`float`
    """

    if input_code == 'CZK':
        return 1 / cnb_czk_currency(output_code)

    if output_code == 'CZK':
        return cnb_czk_currency(input_code)

    inc = cnb_czk_currency(input_code)
    outc = cnb_czk_currency(output_code)
    return inc / outc

def cnb_czk_currency(code):
    """
    Fetch currency of CZK from Czech National Bank.

    :param code: input currency code (three uppercase letters)
    :type: :class:`str`

    :returns: the currency
    :rtype: :class:`float`
    """

    def parse_from(path):
        req = get(BASE + path)
        match = re.search('(\d+)\|{}\|(\d+,\d+)$'.format(code), req.text, re.M)

        if match:
            curr = float(re.sub(',', '.', match[2])) / int(match[1])

            # zero currencies are useless (e. g. for Zimbabwe)
            if curr:
                return curr

        raise NotFound

    BASE = 'https://www.cnb.cz/cs/financni_trhy/devizovy_trh/'

    try:
        return parse_from('kurzy_devizoveho_trhu/denni_kurz.txt')
    except NotFound:
        return parse_from('kurzy_ostatnich_men/kurzy.txt')

def from_yahoo(input_code, output_code):
    """
    Fetch currency from Yahoo Finance API. The currencies look fresh, but there
    is no good documentation about the request parameters.

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: :class:`str`

    :returns: the currency
    :rtype: :class:`float`
    """

    req = get('https://download.finance.yahoo.com/d/quotes?s={}{}=X&f=l1'\
        .format(input_code, output_code))
    return float(req.text)
