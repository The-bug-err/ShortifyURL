# Create your views here.
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .models import UrlMap
import hashlib
import base64
from django.conf import settings


def index(request):
    return render(request, 'shortifyUrl/index.html', {})


def redirect_func(request, tiny_url):
    """
    If a tiny_url is sent with the request, fetch its corresponding original URL
    Redirect to that URL
    """
    if tiny_url:
        try:
            url_obj = UrlMap.objects.get(short_url=tiny_url)
            return redirect(url_obj.original_url)
        except Exception as e:
            return render(request, 'shortifyUrl/index.html',
                          {'some_data': 'Could not find matching URL in DB, Exception : {}'.format(e)})


def shoten_url(original_url, alias=None):
    """
    Use MD5 hash of the original URL to get a unique hash value,
    then encode the hash value to get a possible alias.
    :param original_url: original URL to be shortened.
    :param alias: An alias to be used as tiny URL.
    :return: Shortened version of URL.
    """
    if alias:
        already_exists = list(UrlMap.objects.filter(short_url=alias))
        if already_exists:
            return 0
        else:
            return alias
    hash_object = hashlib.md5(original_url.encode())
    hex_object = hash_object.digest()
    possible_alias = base64.b64encode(hex_object).decode("utf-8")
    return possible_alias


class ShortenURL(ModelViewSet):
    queryset = UrlMap.objects.all()

    # allowed_methods = ['GET']

    def list(self, request, *args, **kwargs):
        try:
            original_url = self.request.query_params.get('url')
            alias = self.request.query_params.get('alias', None)
            tiny_url = str(shoten_url(original_url=original_url, alias=alias))
            if tiny_url == '0':
                return render(request, 'shortifyUrl/index.html', {'some_data': 'The above Alias is already used.'})
            url_lookup = dict(
                short_url=tiny_url,
                original_url=original_url
            )
            new_url, _created = UrlMap.objects.update_or_create(
                defaults=url_lookup,
                **url_lookup
            )
            current_url = settings.ALIAS + '/' + tiny_url
            domain = request.build_absolute_uri().rsplit('/', 1)[0]
            link = domain + '/' + current_url
            return render(request, 'shortifyUrl/index.html', {'some_data': link})
        except Exception as e:
            return render(request, 'shortifyUrl/index.html',
                          {'some_data': 'Exception occurred during the creation of URL {}'.format(e)})

    def create(self, request, *args, **kwargs):
        try:
            return render(request, 'shortifyUrl/index.html', {'some_data': 'Reached Create endpoint.'})
        except Exception as e:
            return render(request, 'shortifyUrl/index.html', {'some_data': 'Exception in create. {}'.format(e)})
