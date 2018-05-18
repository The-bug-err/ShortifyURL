# Create your views here.
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .models import UrlMap
from .utils import UrlUtils
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


class ShortenURL(ModelViewSet):
    queryset = UrlMap.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            original_url = self.request.query_params.get('url')
            # TODO : Validate Original URL
            alias = self.request.query_params.get('alias', None)
            tiny_url = UrlUtils(url=original_url, alias=alias).validate_and_get_tiny_url()
            if tiny_url['type'] == 'error':
                return render(request, 'shortifyUrl/index.html', {'some_data': tiny_url['url']})
            url_lookup = dict(
                short_url=tiny_url['url'],
                original_url=original_url
            )
            new_url, _created = UrlMap.objects.update_or_create(
                defaults=url_lookup,
                **url_lookup
            )
            current_url = settings.ALIAS + '/' + tiny_url['url']
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
