# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as AuthUserCreationForm,
    UserChangeForm as AuthUserChangeForm)
from .models import User


class UserChangeForm(AuthUserChangeForm):
    class Meta(AuthUserChangeForm.Meta):
        model = User


class UserCreationForm(AuthUserCreationForm):
    email = forms.EmailField(label='邮箱')
    username = forms.RegexField(label='昵称',
        regex=r'^([\w\d\-\u2E80-\u9FFF]+){4,20}$',
        help_text= '昵称长度4-20个字符，支持中英文、数字、-、_',
        error_messages={
            'invalid': '昵称长度4-20个字符，支持中英文、数字、-、_'})
    class Meta(AuthUserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            '这个邮箱地址已被注册， 是否忘记密码？'
        )
