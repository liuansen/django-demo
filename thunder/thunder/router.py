# -*-coding:utf-8-*-
from __future__ import unicode_literals

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router_no_slash = DefaultRouter(trailing_slash=False)
