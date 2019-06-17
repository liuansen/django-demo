# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from common.utils import UserWithAvatarSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(UserWithAvatarSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label='邮箱',
                                  required=False, allow_null=True, allow_blank=True)
    mobile = serializers.CharField(label='手机号',
                                   required=False, allow_null=True, allow_blank=True)
    captcha = serializers.CharField(label='验证码',
                                    required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(label='密码',
                                     required=False, allow_null=True, trim_whitespace=False, allow_blank=True)


class MobileSerializer(serializers.Serializer):
    mobile = serializers.RegexField(label='手机号', required=False,
                                    allow_null=True, allow_blank=True,
                                    regex='^(\d{8,11})$',
                                    help_text='不允许重复',
                                    error_messages={
                                        'invalid': '手机格式不正确'})
    mobile_code_id = serializers.RegexField(
        label='区号编号', required=False,
        allow_null=True, allow_blank=True, help_text='区号编号',
        regex='^(\d+)$', error_messages={'invalid': '手机区号格式不正确'})


class CaptchaSerializer(MobileSerializer, serializers.Serializer):
    mobile = serializers.CharField(label='手机号', help_text='手机号不能为空')
    captcha = serializers.CharField(label='验证码', help_text='验证码不能为空')
    mobile_code_id = serializers.CharField(
        label='区号编号', required=False,
        allow_null=True, allow_blank=True, help_text='区号编号')


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='邮箱', max_length=50, required=False, allow_blank=True, allow_null=True,
        error_messages={'invalid': '邮箱格式不正确', 'max_length': '邮箱长度不能超过50个字符'},help_text= '不允许重复')


class SignupSerializer(EmailSerializer, MobileSerializer, serializers.Serializer):
    username = serializers.CharField(
        label='昵称', allow_blank=True, allow_null=True, required=False, help_text='昵称')
    password = serializers.CharField(
        label='密码', allow_blank=True, trim_whitespace=False,
        allow_null=True, required=False, help_text='密码')
    captcha = serializers.CharField(
        label='验证码', allow_blank=True,
        allow_null=True, required=False, help_text='验证码')
    invite_code = serializers.CharField(
        label='注册邀请码', allow_blank=True,
        allow_null=True, required=False, help_text='注册邀请码')


class AdditionalInfoSerializer(serializers.Serializer):
    province = serializers.CharField(
        label='省份', help_text='省份不能为空', error_messages={'blank': '省份信息不能为空'})
    city = serializers.CharField(
        label='城市', help_text='城市不能为空', error_messages={'blank': '城市信息不能为空'})
    district = serializers.CharField(
        label='区县', help_text='区县不能为空', error_messages={'blank': '区县信息不能为空'})
    street = serializers.CharField(
        label='详细住址', help_text='详细住址不能为空', error_messages={'blank': '详细住址信息不能为空'})
    career = serializers.CharField(
        label='职业代码', help_text='职业代码不能为空', error_messages={'blank': '职业信息不能为空'})


class SettingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='昵称', required=False,
                                     allow_null=True, allow_blank=True)
    gender = serializers.ChoiceField(
        choices="(0, '保密'),(1, '男'),(2, '女')", help_text="(0, '保密'),(1, '男'),(2, '女')")
    career = serializers.CharField(label='职业', required=False,
                                   allow_null=True, allow_blank=True)
    email = serializers.CharField(label='邮箱', required=False,
                                  allow_null=True, allow_blank=True)
    qq = serializers.CharField(label='qq', required=False,
                               allow_null=True, allow_blank=True)
    mobile = serializers.SerializerMethodField('hidden_mobile')

    class Meta:
        model = User
        fields = ('id', 'username', 'province', 'city', 'gender', 'description',
                  'mobile', 'is_password_set', 'is_trade_password_set', 'date_joined',
                  'birthday', 'email', 'qq', 'we_chat', 'we_bo', 'street', 'career', 'district' )
        read_only_fields = ('is_password_set', 'is_trade_password_set', 'date_joined')

    def hidden_mobile(self, obj):
        if obj.mobile:
            return obj.mobile[:3] + "*" * 4 + obj.mobile[-4:]
        else:
            return None
