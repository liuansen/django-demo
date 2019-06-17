# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .forms import *
from common.custom_model_admin import CustomModelAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User
# Register your models here.


class UserAdmin(CustomModelAdmin, AuthUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )
    list_display = ['id', 'username', 'mobile_code', 'mobile',
                    'avatar_thumb', 'email', 'is_active', 'date_joined']
    ordering = ['-id']
    search_fields = ['username', 'mobile', ]
    list_filter = ('is_superuser', 'is_system',)

    def avatar_thumb(self, obj):
        if obj.avatar:
            return '<a href="%s" target="_blank"><img src="%s"/></a>' % (obj.avatar.url_640x640, obj.avatar.url_80x80,)
        return ''

    avatar_thumb.short_description = '头像'
    avatar_thumb.allow_tags = True


admin.site.register(User, UserAdmin)
