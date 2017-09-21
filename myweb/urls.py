"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


from exam.core import rest as restView

from exam.views import HomePageView
from exam.views import easyfunction

from music.views import hello


urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^music/', include('music.urls')),
    url(r'^music/hello/', hello),

    url(r'^exam/', include('exam.urls')),

    url(r'^exam/?$', HomePageView.as_view()),
    url(r'^exam/car/', easyfunction),

    url(r'^exam/rest/?$', restView.Operation.as_view()),
    url(r'^exam/rest/header/', restView.ExtractHeader.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
