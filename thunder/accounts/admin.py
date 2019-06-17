# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .forms import *
from common.custom_model_admin import CustomModelAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User
# Register your models here.



