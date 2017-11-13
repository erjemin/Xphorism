# -*- coding: utf-8 -*-
__author__ = 'Sergei Erjemin'

from django.conf.urls import url, include
from django.contrib import admin
from Xphorism import settings
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url( r'^$', views.start ),
    url( r'^x5[/]$', views.x5 ),
    url( r'^getPersonContact/(?P<ContactID>\d{1,})$', views.getPersonContact ),
    url( r'^avaho[/]$', views.avaho ),

]

#  ___    ____      _              _____         _ _              _____             _
# | | |  |    \ ___| |_ _ _ ___   |_   _|___ ___| | |_ ___ ___   |  _  |___ ___ ___| |
# |_  |  |  |  | -_| . | | | . |    | | | . | . | | . | .'|  _|  |   __| .'|   | -_| |
#   |_|  |____/|___|___|___|_  |    |_| |___|___|_|___|__,|_|    |__|  |__,|_|_|___|_|
#                          |___|
if settings.DEBUG:
    import debug_toolbar
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
