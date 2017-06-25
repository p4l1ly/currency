"""
TODO
"""

import re
from decimal import Decimal
from functools import partial
from .helpers import get
import currency.symbol_dict as symbol_dict

class NotFound(Exception): pass

def currency(input_repr, output_repr):
    """
    Get currency by all implemented means (from modules :mod:`currency.fetcher`
    and :mod:`currency.symbol_dict`) to get the currency. The least reliable of
    all functions is :fun:`symbol_dict.from_xe` (it is only parsing of a online
    html, internals of which may change anytime and the connection is not even
    secured). We use it only if all other methods fail.

    :param input_repr: input currency code or symbol
    :type input_code: :class:`str`

    :param output_repr: output currency code or symbol
    :type output_code: :class:`str`

    :returns: the currency
    :rtype: :class:`decimal.Decimal`
    """

    input_code = symbol_dict.repr_to_code(input_repr)
    output_code = symbol_dict.repr_to_code(output_repr)

    if input_code and output_code:
        return from_all(input_code, output_code)

    # the input_code is known, the output_code is unknown
    if input_code:
        if re.search('^[A-Z]{3}$', output_repr):
            try:
                return from_all(input_code, output_repr)
            except:
                output_code = symbol_dict.from_xe(output_repr)
                return from_all(input_code, output_code)

        else:
            output_code = symbol_dict.from_xe(output_repr)
            return from_all(input_code, output_code)

    # the output_code is known, the input_code is unknown
    if output_code:
        if re.search('^[A-Z]{3}$', input_repr):
            try:
                return from_all(input_repr, output_code)
            except:
                input_code = symbol_dict.from_xe(input_repr)
                return from_all(input_code, output_code)

        else:
            input_code = symbol_dict.from_xe(input_repr)
            return from_all(input_code, output_code)

    # both codes are unknown
    input_might_be_code, output_might_be_code =\
        map(partial(re.search, '^[A-Z]{3}$'), [input_repr, output_repr])

    if input_might_be_code and output_might_be_code:
        try:
            return from_all(input_repr, output_repr)
        except:
            input_code = symbol_dict.from_xe(input_repr)
            output_code = symbol_dict.from_xe(output_repr)
            return from_all(input_code, output_code)

    if input_might_be_code:
        output_code = symbol_dict.from_xe(output_repr)
        try:
            return from_all(input_repr, output_code)
        except:
            input_code = symbol_dict.from_xe(input_repr)
            return from_all(input_code, output_code)

    if output_might_be_code:
        input_code = symbol_dict.from_xe(input_repr)
        try:
            return from_all(input_code, output_repr)
        except:
            output_code = symbol_dict.from_xe(output_repr)
            return from_all(input_code, output_code)

    # both inputs are unable to be translated by symbol_dict.currency and they
    # cannot be currency codes. Let's try to translate them by
    # :fun:`symbol_dict.from_xe`.
    input_code = symbol_dict.from_xe(input_repr)
    output_code = symbol_dict.from_xe(output_repr)
    return from_all(input_repr, output_code)

def from_all(input_code, output_code):
    """
    Try all implemented techniques to get as good currency as possible. The
    first pick is Yahoo. If it fails, fixer.io and cnb.cz are used as fallbacks.

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: :class:`str`

    :returns: the currency
    :rtype: :class:`decimal.Decimal`
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
    :rtype: :class:`decimal.Decimal`
    """

    req = get('https://api.fixer.io/latest?base={}&symbols={}'.format(
        input_code, output_code))

    return req.json(parse_float=Decimal)['rates'][output_code]

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
    :rtype: :class:`decimal.Decimal`
    """

    if input_code == 'CZK':
        return Decimal('1') / cnb_czk_currency(output_code)

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
    :rtype: :class:`decimal.Decimal`
    """

    def parse_from(path):
        req = get(BASE + path)
        match = re.search('(\d+)\|{}\|(\d+,\d+)$'.format(code), req.text, re.M)

        if match:
            curr = Decimal(re.sub(',', '.', match[2])) / int(match[1])

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
    :rtype: :class:`decimal.Decimal`
    """

    req = get('https://download.finance.yahoo.com/d/quotes?s={}{}=X&f=l1'\
        .format(input_code, output_code))
    return Decimal(req.text)
