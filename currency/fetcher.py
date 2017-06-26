# -*- coding: utf-8 -*-

u"""
This modules provides functions to fetch money currencies from various online
APIs.
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

import re
from decimal import Decimal
from functools import partial
from .helpers import get
import currency.symbol_dict as symbol_dict

class NotFound(Exception): pass

def currency(input_repr, output_repr):
    u"""
    Get currency by all implemented means (from modules :mod:`currency.fetcher`
    and :mod:`currency.symbol_dict`) to get the currency. The least reliable of
    all functions is :func:`currency.symbol_dict.from_xe` (it is only parsing of
    a online html, internals of which may change anytime and the connection is
    not even secured). We use it only if all other methods fail.

    :param input_repr: input currency code or symbol
    :type input_code: :class:`str`

    :param output_repr: output currency code or symbol
    :type output_code: :class:`str`

    :returns: input code, output code and the currency
    :rtype: (:class:`str`, :class:`str`, :class:`decimal.Decimal`)
    """

    def get_result(input_code, output_code):
        try:
            return input_code, output_code, from_all(input_code, output_code)
        except (IndexError, NotFound):
            return input_code, output_code, None

    input_code = symbol_dict.repr_to_code(input_repr)
    output_code = symbol_dict.repr_to_code(output_repr)

    if input_code and output_code:
        return get_result(input_code, output_code)

    # the input_code is known, the output_code is unknown
    if input_code:
        if re.search(u'^[A-Z]{3}$', output_repr):
            try:
                return get_result(input_code, output_repr)
            except:
                output_code = symbol_dict.from_xe(output_repr)
                return get_result(input_code, output_code)

        else:
            output_code = symbol_dict.from_xe(output_repr)
            return get_result(input_code, output_code)

    # the output_code is known, the input_code is unknown
    if output_code:
        if re.search(u'^[A-Z]{3}$', input_repr):
            try:
                return get_result(input_repr, output_code)
            except:
                input_code = symbol_dict.from_xe(input_repr)
                return get_result(input_code, output_code)

        else:
            input_code = symbol_dict.from_xe(input_repr)
            return get_result(input_code, output_code)

    # both codes are unknown
    input_might_be_code, output_might_be_code =\
        map(partial(re.search, u'^[A-Z]{3}$'), [input_repr, output_repr])

    if input_might_be_code and output_might_be_code:
        try:
            return get_result(input_repr, output_repr)
        except:
            input_code = symbol_dict.from_xe(input_repr)
            output_code = symbol_dict.from_xe(output_repr)
            return get_result(input_code, output_code)

    if input_might_be_code:
        output_code = symbol_dict.from_xe(output_repr)
        try:
            return get_result(input_repr, output_code)
        except:
            input_code = symbol_dict.from_xe(input_repr)
            return get_result(input_code, output_code)

    if output_might_be_code:
        input_code = symbol_dict.from_xe(input_repr)
        try:
            return get_result(input_code, output_repr)
        except:
            output_code = symbol_dict.from_xe(output_repr)
            return get_result(input_code, output_code)

    # both inputs are unable to be translated by symbol_dict.currency and they
    # cannot be currency codes. Let's try to translate them by
    # symbol_dict.from_xe.
    input_code = symbol_dict.from_xe(input_repr)
    output_code = symbol_dict.from_xe(output_repr)
    return get_result(input_repr, output_code)

def all_currencies(input_repr, yahoo=False):
    u"""
    Get all currencies with base **input_repr**. As sources of the currencies
    use functions :func:`from_fixer_all_outputs` and
    :func:`currency.fetcher.from_cnb_all_outputs`. Yahoo source can be also used
    to get more currencies, which are in addition more fresh, but it slows down
    the fetch quite a lot.

    :param input_repr: input currency code or symbol
    :type input_repr: :class:`str`

    :param yahoo: use :func:`currency.fetcher.from_yahoo` as a source (place it
                  between fixer and cnb)
    :type yahoo: :class:`bool`

    :returns: input code, output code and dict of currencies
    :rtype: (:class:`str`, :class:`str`,
        :class:`dict` <:class:`str` : :class:`decimal.Decimal`>)
    """
    try:
        input_code = symbol_dict.from_all(input_repr)
    except:
        input_code = input_repr

    try:
        result = from_fixer_all_outputs(input_code)
    except:
        result = {}

    try:
        cnb_result = from_cnb_all_outputs(input_code)
    except:
        cnb_result = {}

    def from_cnb_dict(input_code, output_code):
        return cnb_result[output_code]

    failed = []

    for output_code in symbol_dict.locale.currencies:
        if output_code not in result:
            sources = [from_yahoo, from_cnb_dict] if yahoo else [from_cnb_dict]
            try:
                result[output_code] = from_all(input_code, output_code, sources)
            except:
                failed.append(output_code)

    return input_code, result, failed

def from_fixer_all_outputs(input_code):
    u"""
    Fetch all currencies with given base from JSON API at https://api.fixer.io

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :returns: dict of currencies
    :rtype: :class:`dict` <:class:`str` : :class:`decimal.Decimal`>
    """
    req = get(u'https://api.fixer.io/latest?base={}'.format(input_code))
    return req.json(parse_float=Decimal)[u'rates']

def from_fixer(input_code, output_code):
    u"""
    Fetch currency from JSON API at https://api.fixer.io

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: :class:`str`

    :returns: the currency
    :rtype: :class:`decimal.Decimal`
    """

    req = get(u'https://api.fixer.io/latest?base={}&symbols={}'.format(
        input_code, output_code))

    return req.json(parse_float=Decimal)[u'rates'][output_code]

def from_cnb(input_code, output_code):
    u"""
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

    if input_code == u'CZK':
        return Decimal('1') / cnb_czk(output_code)

    if output_code == u'CZK':
        return cnb_czk(input_code)

    inc = cnb_czk(input_code)
    outc = cnb_czk(output_code)
    return inc / outc

class CNB:
    u"""
    Czech National Bank webpage URLs
    """
    BASE = u'https://www.cnb.cz/cs/financni_trhy/devizovy_trh/'
    DAILY = u'kurzy_devizoveho_trhu/denni_kurz.txt'
    MONTHLY = u'kurzy_ostatnich_men/kurzy.txt'

def from_cnb_all_outputs(input_code):
    u"""
    Fetch all currencies with given base from Czech National Bank.

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :returns: dict of currencies
    :rtype: :class:`dict` <:class:`str` : :class:`decimal.Decimal`>
    """

    result = {}

    for path in [CNB.DAILY, CNB.MONTHLY]:
        req = get(CNB.BASE + path)
        for match in re.finditer(u'(\d+)\|([^|]+)\|(\d+,\d+)$', req.text, re.M):
            curr = Decimal(re.sub(u',', u'.', match.group(3))) \
                 / int(match.group(1))
            if curr:
                result[match.group(2)] = curr

    if input_code == u'CZK':
        return {k: Decimal(u'1') / v for k, v in result.items()}
    else:
        inc = result[input_code]
        result[u'CZK'] = 1
        return {k: inc / outc for k, outc in result.items()}

def cnb_czk(code):
    u"""
    Fetch currency of CZK from Czech National Bank.

    :param code: input currency code (three uppercase letters)
    :type: :class:`str`

    :returns: the currency
    :rtype: :class:`decimal.Decimal`
    """

    def parse_from(path):
        req = get(CNB.BASE + path)
        match = re.search(u'(\d+)\|{}\|(\d+,\d+)$'.format(code), req.text, re.M)

        if match:
            curr = Decimal(re.sub(u',', u'.', match.group(2))) \
                 / int(match.group(1))

            # zero currencies are useless (e. g. for Zimbabwe)
            if curr:
                return curr

        raise NotFound

    try:
        return parse_from(CNB.DAILY)
    except NotFound:
        return parse_from(CNB.MONTHLY)

def from_yahoo(input_code, output_code):
    u"""
    Fetch currency from Yahoo Finance API. The currencies look fresh, but there
    is no good documentation about the request parameters.

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: :class:`str`

    :returns: the currency
    :rtype: :class:`decimal.Decimal`
    """

    req = get(u'https://download.finance.yahoo.com/d/quotes?s={}{}=X&f=l1'\
        .format(input_code, output_code))
    return Decimal(req.text)

def from_all(input_code, output_code,
    sources=[from_yahoo, from_fixer, from_cnb]):
    u"""
    Try all implemented techniques (it can be limited by the **sources**
    parameter) to get as good currency as possible.

    :param input_code: input currency code (three uppercase letters)
    :type input_code: :class:`str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: :class:`str`

    :param sources: Try to fetch by the first source, the others are fallbacks
    :type sources: :class:`list` < :class:`function`
        (:class:`str`, :class:`str`) ⟶ :class:`decimal.Decimal` >

    :returns: the currency
    :rtype: :class:`decimal.Decimal`
    """

    for fetch in sources:
        try:
            return fetch(input_code, output_code)
        except Exception as e:
            err = e

    raise err
