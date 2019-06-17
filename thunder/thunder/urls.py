# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import include, url

from common.api_docs_utils import get_swagger_view

admin.autodiscover()

urlpatterns = [
    url(r'^api/v1/', include('thunder.api_urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^docs/', get_swagger_view(title='My great API')),
    url(r'^admin/', include(admin.site.urls)),
]
