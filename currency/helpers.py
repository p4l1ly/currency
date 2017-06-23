"""
TODO
"""

import requests

def get(addr):
    """
    make GET request, close it and if something fails, raise exception

    :param addr: request URL
    :type addr: :class:`str`

    :returns: the closed response object with status code 200 OK
    :rtype: :class:`requests.Response`

    :raises: :class:`requests.RequestException`
    """
    r = requests.get(addr)
    r.close()
    r.raise_for_status()
    return r
