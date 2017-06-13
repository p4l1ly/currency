import re
from enum import Enum
from .helpers import get

class NotFound(Exception): pass

class FetchMode(Enum):
    "Enumeration for `fetch_currency`"
    RELIABLE = 1
    LATEST = 2

def from_all(input_code, output_code, mode=FetchMode.RELIABLE):
    """
    try all implemented techniques to get as good currency as possible

    :param input_code: input currency code (three uppercase letters)
    :type input_code: `str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: `str`

    :param mode: For some currencies there is a problem to get the latest values
        from some free API. With mode=FetchMode.RELIABLE, it is prefered to get
        these values from servers that offer the data that are not so fresh, but
        they are provided in a standardized format and the servers are secured.
        With mode=FetchMode.LATEST it is prefered to find the values in html
        pages, internals of which may change and the values may be misleading.
    :type mode: `FetchMode`

    :type input_code: `FetchMode`

    :returns: the currency
    :rtype: `float`
    """

    if mode is FetchMode.RELIABLE:
        fetches = [fetch_from_cnb, fetch_from_fixer, fetch_from_xe]
    elif mode is FetchMode.LATEST:
        fetches = [fetch_from_fixer, fetch_from_xe, fetch_from_cnb]
    else:
        raise TypeError('mode should be of FetchMode enum type')

    for fetch in fetches:
        try:
            return fetch(input_code, output_code)
        except Exception as e:
            pass

    raise e

def from_fixer(input_code, output_code):
    """
    Fetch currency from JSON API at http://api.fixer.io

    :param input_code: input currency code (three uppercase letters)
    :type input_code: `str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: `str`
    """

    req = get('http://api.fixer.io/latest?base={}&symbols={}'.format(
        input_code, output_code))

    return req.json()['rates'][output_code]

def from_cnb(input_code, output_code):
    """
    Fetch currency from Czech National Bank. This is the only https connection,
    so it is considered the most reliable. The currencies are not very fresh and
    they are rounded to three decimal places.

    :param input_code: input currency code (three uppercase letters)
    :type input_code: `str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: `str`
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
    :type: `str`
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
