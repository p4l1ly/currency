"""
This module contains unsorted simple helper functions used in currency
converter.
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
