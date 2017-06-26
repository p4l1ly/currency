"""
This modules provides functions to convert currency symbols into currency codes.
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

from lxml import html
from .helpers import get
import os
import babel

locale = babel.Locale('en', 'US')

up = os.path.dirname
STATIC_PATH = os.path.join(up(os.path.realpath(__file__)), 'symbols.html')

def repr_to_code(code_or_sym):
    """
    Take arbitrary currency representation (currency code or symbol). If it is a
    code, return it. If it is a symbol, try to use :func:`from_babel` and
    :func:`from_static` to convert it to the currency code.

    :param symbol: currency symbol or code
    :type symbol: :class:`str`

    :returns: currency code or :class:`None` if unsuccessful
    :rtype: :class:`str` or :class:`None`
    """
    if code_or_sym in locale.currencies:
        return code_or_sym

    try:
        return from_babel(code_or_sym)
    except KeyError:
        try:
            return from_static(code_or_sym)
        except KeyError:
            return None

def from_all(symbol):
    """
    Convert currency symbol into currency code. Try to find it with babel
    library, use :func:`currency.symbol_dict.from_xe` and
    :func:`currency.symbol_dict.from_static` as fallbacks.

    :param symbol: symbol to convert
    :type symbol: :class:`str`

    :returns: currency code
    :rtype: :class:`str`
    """
    for dict_fn in [from_babel, from_xe, from_static]:
        try:
            return dict_fn(symbol)
        except Exception as e:
            err = e

    raise err

def from_babel(symbol):
    """
    Use babel library with en.US locale to convert the symbol into currency
    code.

    :param symbol: symbol to convert
    :type symbol: :class:`str`

    :returns: currency code
    :rtype: :class:`str`
    """
    # lazy loading of babel table
    if not hasattr(from_babel, 'table'):
        from_babel.table = {symbol: code
            for code, symbol in locale.currency_symbols.items()}

    return from_babel.table[symbol]

def from_xe(symbol):
    """
    Scrap page http://www.xe.com/symbols.php containing a currency table to
    convert the symbol into currency code.

    :param symbol: symbol to convert
    :type symbol: :class:`str`

    :returns: currency code
    :rtype: :class:`str`
    """
    text = get('http://www.xe.com/symbols.php').text
    root = html.fromstring(text)
    return root.xpath("""
        .//table[@class="currencySymblTable"]
        /tr[@class="row1" or @class="row2"]
        /td[6][text()="{}"]/..
        /td[2]/text()
        """.format(symbol_ords(symbol)))[0]

def symbol_ords(symbol):
    """
    Convert utf8 string into string of decimal ordinal representations of each
    character separated by comma.

    :param symbol: string to convert
    :type symbol: :class:`str`

    :returns: decimal ordinal representations of each input character
    :rtype: :class:`str` (integers separated by commas)
    """
    return ', '.join(str(ord(x)) for x in symbol)

def xe_to_dict(root):
    """
    Convert the static page (downloaded from http://www.xe.com/symbols.php on
    13th June 2017) into symbol to code table in form of Python :class:`dict`
    for simplicity and performance.

    :param root: root node of html page
    :type root: :class:`lxml.html.HtmlElement`

    :returns: dictionary that maps currency symbols to currency codes
    :rtype: :class:`dict` <:class:`str`: :class:`str`>
    """
    rows = root.xpath("""
        .//table[@class="currencySymblTable"]
        /tr[@class="row1" or @class="row2"]""")

    def symbol(tr):
        bs = tr.xpath('td[6]/text()')[0].split(', ')
        return ''.join(chr(int(x)) for x in bs)

    def code(tr):
        return tr.xpath('td[2]/text()')[0]

    def keyval(tr):
        try:
            return symbol(tr), code(tr)
        except IndexError: # some data are missing in the table
            return None

    return {kv[0]: kv[1] for kv in map(keyval, rows) if kv}

def from_static(symbol):
    """
    Use static table (downloaded from http://www.xe.com/symbols.php on 13th June
    2017) to convert the symbol into currency code.

    :param symbol: symbol to convert
    :type symbol: :class:`str`

    :returns: currency code
    :rtype: :class:`str`
    """

    # lazy loading of static table
    if not hasattr(from_static, 'table'):
        from_static.table = xe_to_dict(html.parse(STATIC_PATH))

    return from_static.table[symbol]
