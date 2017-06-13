from enum import Enum
import requests

class NoSuccess(Exception): pass

class FetchMode(Enum):
    "Enumeration for `fetch_currency`"
    RELIABLE = 1
    LATEST = 2

def fetch_currency(input_code, output_code, mode=FetchMode.RELIABLE):
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


def fetch_from_fixer(input_code, output_code):
    """
    Fetch currency from JSON API at http://api.fixer.io, for example
    http://api.fixer.io/latest?base=EUR&symbols=USD

    :param input_code: input currency code (three uppercase letters)
    :type input_code: `str`

    :param output_code: output currency code (three uppercase letters)
    :type input_code: `str`
    """

    req = requests.get('api.fixer.io/latest?base={}&symbols={}'.format(
        input_code, output_code))
    req.raise_for_status()
    req.close()

    return data.json()['rates'][output_code]
