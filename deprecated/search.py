"""
Deprecated social media search functions.

These functions use Google Custom Search API to search for names
on Google, Facebook, and Instagram. They are no longer maintained
as part of the core kuaci library.

Usage requires a Google Custom Search API key.
See: https://developers.google.com/custom-search/v1/using_rest
"""

import requests
from furl import furl

CX = '013743239855164640998:wdyn0oqb1ia'
BASE_URL = 'https://www.googleapis.com/customsearch/v1'


def _search(name, key, site=None, exact_match=True):
    f = furl(BASE_URL)
    f.args['key'] = key
    f.args['cx'] = CX
    f.args['q'] = name
    if exact_match:
        f.args['exactTerms'] = name
    if site:
        f.args['siteSearch'] = site

    response = requests.get(f.url)
    return response.json()['queries']['request'][0]['totalResults']


def google_search(name, key, exact_match=True):
    return _search(name, key, exact_match=exact_match)


def facebook_search(name, key, exact_match=True):
    return _search(name, key, site='www.facebook.com', exact_match=exact_match)


def instagram_search(name, key, exact_match=True):
    return _search(name, key, site='www.instagram.com', exact_match=exact_match)
