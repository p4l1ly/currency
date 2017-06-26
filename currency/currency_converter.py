# -*- coding: utf-8 -*-

u"""
Currency converter CLI application. For more detailed interface description see
:doc:`README <index>`.

**Example command**:

.. sourcecode:: sh

   python scripts/currency_converter.py --amount 10 --input_currency € --output_currency CZK

**Example result**:

.. sourcecode:: json

   {
       u"input": {
           u"amount": 10,
           u"currency": u"EUR"
       },
       u"output": {
           u"CZK": 262.4100
       }
   }

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

import argparse
import decimal
import currency.app as currency
import sys
from builtins import str

def main():
    u"""
    Parse command line arguments and evaluate the :func:`currency.app.app`
    function.

    :result: pretty formatted JSON string, as described in :doc:`README <index>`
    :rtype: :class:`str`
    """

    parser = argparse.ArgumentParser(description=u'Currency converter')

    parser.add_argument(u"--amount", type=decimal.Decimal, required=True,
        help=u"Amount of money to convert.")

    parser.add_argument(u"--input_currency", type=str, required=True,
        help=u"The currency of the money you want to convert.")

    parser.add_argument(u"--output_currency", type=str,
        help=u"""\
        The currency of the money you want to get from the conversion.
        If omitted, convert to all known currencies.
        """)

    args = parser.parse_args()

    return currency.app(
        args.amount, args.input_currency, args.output_currency)
