# -*- coding: utf-8 -*-

u"""
This module contains unsorted simple helper functions used in currency
converter.
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

import requests

def get(addr):
    u"""
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
