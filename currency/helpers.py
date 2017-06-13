import requests

def get(addr):
    r = requests.get(addr)
    r.raise_for_status()
    r.close()
    return r
