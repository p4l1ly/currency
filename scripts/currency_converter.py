#! /usr/bin/python

"""
Currency converter CLI application. For more detailed interface description see
:doc:`README <index>`.

**Example command**:

.. sourcecode:: sh

   python scripts/currency_converter.py --amount 10 --input_currency € --output_currency CZK

**Example result**:

.. sourcecode:: json

   {
       "input": {
           "amount": 10,
           "currency": "EUR"
       },
       "output": {
           "CZK": 262.4100
       }
   }

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

import argparse
import decimal
import currency.app as currency
import sys

def main():
    """
    Parse command line arguments and evaluate the :func:`currency.app.app`
    function.

    :result: pretty formatted JSON string, as described in :doc:`README <index>`
    :rtype: :class:`str`
    """

    parser = argparse.ArgumentParser(description='Currency converter')

    parser.add_argument("--amount", type=decimal.Decimal, required=True,
        help="Amount of money to convert.")

    parser.add_argument("--input_currency", type=str, required=True,
        help="The currency of the money you want to convert.")

    parser.add_argument("--output_currency", type=str,
        help="""\
        The currency of the money you want to get from the conversion.
        If omitted, convert to all known currencies.
        """)

    args = parser.parse_args()

    return currency.app(
        args.amount, args.input_currency, args.output_currency)

if __name__ == '__main__':
    print(main())
