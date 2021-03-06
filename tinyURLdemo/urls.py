"""tinyURLdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from shortifyUrl import views as shortifyViews
from django.conf import settings


REDIRECT_REGEX = '^{}'.format(settings.ALIAS)
urlpatterns = [
    url('admin/', admin.site.urls),    # citrix_user citrix@1
    url(r'^$', shortifyViews.index, name='index'),
    url(r'^generate', shortifyViews.ShortenURL.as_view({'get': 'list'}), name='generate'),
    url('^{}/(?P<tiny_url>.*)'.format(settings.ALIAS), shortifyViews.redirect_func, name='redirect')
]
