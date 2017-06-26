#! /usr/bin/python

import currency.fetcher
import argparse
import decimal
import simplejson as json

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

    def pretty_print(inp, outp):
        data = { 'input': {'amount': args.amount, 'currency': inp}
               , 'output': outp }
        print(json.dumps(data, indent=4, sort_keys=True))

    if args.output_currency:
        input_code, output_code, curr =\
            currency.fetcher.currency(args.input_currency, args.output_currency)
        pretty_print(input_code, {output_code: curr * args.amount})

    else:
        input_code, currs, failed =\
            currency.fetcher.all_currencies(
                args.input_currency, args.output_currency)

        for code, curr in currs.items():
            currs[code] = curr * args.amount

        pretty_print(input_code, currs)

if __name__ == '__main__':
    main()
