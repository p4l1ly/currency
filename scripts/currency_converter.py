#! /usr/bin/python

import argparse
import decimal
import currency.app as currency
import sys

def main():
    "run CLI application"

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
