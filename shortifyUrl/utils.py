"""
Utility methods used by Views
"""

import base64
import hashlib
from .models import UrlMap
from urllib.parse import urlparse


class UrlUtils:
    def __init__(self, url, alias=None):
        self._url = url
        self._alias = alias
        self._tinyUrl = dict(
            type='',
            url=''
        )

    def validate_and_get_tiny_url(self):
        if self.validate():
            self.shoten_url()
        else:
            self._tinyUrl['type'] = 'error'
            self._tinyUrl['url'] = 'The provided URL is not of proper format'
        return self._tinyUrl

    def validate(self):
        pieces = urlparse(self._url)
        if all([pieces.scheme, pieces.netloc]):
            return True
        else:
            return False

    def shoten_url(self):
        """
        Use MD5 hash of the original URL to get a unique hash value,
        then encode the hash value to get a possible alias.
        """
        if self._alias:
            already_exists = list(UrlMap.objects.filter(short_url=self._alias))
            if already_exists:
                self._tinyUrl['type'] = 'error'
                self._tinyUrl['url'] = 'The provided Alias is already used.'
            else:
                self._tinyUrl['type'] = 'success'
                self._tinyUrl['url'] = self._alias
        else:
            hash_object = hashlib.md5(self._url.encode())
            hex_object = hash_object.digest()
            self._tinyUrl['type'] = 'success'
            self._tinyUrl['url'] = base64.b64encode(hex_object).decode("utf-8")
