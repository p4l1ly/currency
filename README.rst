Currency Converter
==================

This project contains a CLI application and a web server for API of currency
converter.

Parameters
**********
- **amount** - amount which we want to convert - float
- **input_currency** - input currency - 3 letters name or currency symbol
- **output_currency** - requested/output currency - 3 letters name or currency
  symbol; if **output_currency** parameter is missing, the application
  converts into all known currencies

Output
******
- json with following structure.

.. code::

    {
        "input": {
            "amount": <float>,
            "currency": <3 letter currency code>
        }
        "output": {
            <3 letter currency code>: <float>
        }
    }

Examples
********
CLI
---
.. code::

    ./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
    {
        "input": {
            "amount": 100.0,
            "currency": "EUR"
        },
        "output": {
            "CZK": 2707.36,
        }
    }

    ./currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
    {
        "input": {
            "amount": 0.9,
            "currency": "CNY"
        },
        "output": {
            "AUD": 0.20,
        }
    }

    ./currency_converter.py --amount 10.92 --input_currency £
    {
        "input": {
            "amount": 10.92,
            "currency": "GBP"
        },
        "output": {
            "EUR": 14.95,
            "USD": 17.05,
            "CZK": 404.82,
            .
            .
            .
        }
    }

API
---

.. code::

    GET /currency_converter?amount=0.9&input_currency=¥&output_currency=AUD HTTP/1.1
    {
        "input": {
            "amount": 0.9,
            "currency": "CNY"
        },
        "output": {
            "AUD": 0.20,
        }
    }

    GET /currency_converter?amount=10.92&input_currency=£ HTTP/1.1
    {
        "input": {
            "amount": 10.92,
            "currency": "GBP"
        },
        "output": {
            "EUR": 14.95,
            "USD": 17.05,
            "CZK": 404.82,
            .
            .
            .
        }
    }
