# -*-coding:utf-8-*-
from __future__ import unicode_literals

import re
from collections import OrderedDict
import pypinyin

from rest_framework import serializers
from django.conf import settings
from common.api import APIResponse
from rest_framework import pagination
from accounts.models import MobileCode
from django.db.models import Max, Min

from accounts.models import User


def verify_usernamge(username):
    '''
    判断用户设置的昵称是否已被占用
    '''
    try:
        User.objects.get(username=username)
        return {'username_used':['该昵称已被注册']}
    except User.DoesNotExist:
        return False


class UserWithAvatarSerializer(serializers.ModelSerializer):
    '''用户头像序列化类'''
    avatar_xs = serializers.CharField(source='avatar.url_80x80', required=False, help_text='选填')
    avatar_sm = serializers.CharField(source='avatar.url_160x160', required=False, help_text='选填')
    avatar_md = serializers.CharField(source='avatar.url_320x320', required=False, help_text='选填')
    avatar_lg = serializers.CharField(source='avatar.url_640x640', required=False, help_text='选填')


class CustomPaginationSerializer(pagination.PageNumberPagination):

    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_paginated_data(self, data):
        return OrderedDict([
            ('total_count', self.page.paginator.count),
            ('total_page', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('results', data)
        ])

    def get_paginated_response(self, data):
        return APIResponse(self.get_paginated_data(data))


def verify_captcha(captcha_key, captcha_value):
    '''
    验证码校验, 支持手机/邮箱/图形验证码校验
    '''
    error_dict = 0

    if not captcha_value:
        error_dict = {'captcha_not_blank': ['验证码不能为空']}
    else:
        # if settings.ENABLE_VERIFY_CAPTCHA:
        #     server_captcha = get_redis_conn().get(captcha_key)
        # else:
        server_captcha = '1234'

        # server_captcha = '123456'
        # if captcha_value != server_captcha:
        #     server_captcha = get_redis_conn().get(captcha_key)

        if server_captcha != captcha_value:
            error_dict = {'captcha_error': ['验证码有误或已过期']}
        else:
            # get_redis_conn().delete(captcha_key)
            pass

    return error_dict


def private_invite_code(invite_code_key, invite_code):
    """
    内测邀请码校验
    :param invite_code_key:
    :param invite_code:
    :return:
    """
    error_dict = 0

    if not invite_code:
        error_dict = {'captcha_not_blank': ['内测邀请码不能为空']}
    else:
        # if settings.ENABLE_VERIFY_CAPTCHA:
        #     server_captcha = get_redis_conn().get(captcha_key)
        # else:
        server_invite = '616833686'

        # server_captcha = '123456'
        # if captcha_value != server_captcha:
        #     server_captcha = get_redis_conn().get(captcha_key)

        if server_invite != invite_code:
            error_dict = {'captcha_error': ['内测邀请码有误或已过期']}
        else:
            # get_redis_conn().delete(captcha_key)
            pass

    return error_dict


def is_email(email):
    # if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email.strip()) == None:
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email.strip()) == None:
        return False
    return True


MOBILE_CODE_CHINA_MAINLAND = 1


def china_mobile_head(include_virtual=False):
    if include_virtual:
        return "((1[38][0-9])|(14[579])|(15[0-3,5-9])|(166)|(17[0-9])|(19[89])|(17[3,5-8]))"
    return "((1[38][0-9])|(14[579])|(15[0-3,5-9])|(166)|(17[3,5-8])|(19[89])|(17[0-9]))"


def is_mobile(mobile, mobile_code=MOBILE_CODE_CHINA_MAINLAND, include_virtual=False):
    '''手机号校验'''
    if not mobile_code:
        check = MobileCode.objects.aggregate(min_len=Min('min_digit'),
            max_len=Max('max_digit'))
        min_digit = check['min_len']
        max_digit = check['max_len']
    else:
        if mobile_code == MOBILE_CODE_CHINA_MAINLAND:
            return re.match("^(%s\\d{8})$" % china_mobile_head(
                include_virtual), mobile.strip()) <> None
        else:
            try:
                check = MobileCode.objects.get(pk=mobile_code)
            except MobileCode.DoesNotExist:
                return False
            min_digit = check.min_digit
            max_digit = check.max_digit
    return re.match("^(\d{%d,%d})$" % (min_digit, max_digit), mobile.strip()) <> None


def generate_number_random(count):
    import random

    items = random.sample('0123456789', count)

    result = ""
    for item in items:
        result += item
    return result


def is_right_string(str):
    '''判断是否为合法字符，支持中英文、数字、-、_，str需为unicode编码'''
    return re.match("^([a-zA-Z0-9-_\u4e00-\u9fa5]+)$", str) != None


def generate_username(username):
    if not username:
        username = "用户" + generate_number_random(8)
    else:
        str = ""
        for s in unicode(username):
            if is_right_string(s):
                str += s
        username = str if str else generate_number_random(8)

    uname = unicode(username.strip())

    if re.match(r'^[0-9]+$', uname):
        username = "用户" + username
    if len(uname.encode('gbk')) < 4:
        username = username + generate_number_random(3)
    if len(uname.encode('gbk')) > 20:
        username = username[0:4] + generate_number_random(3)

    try:
        User.objects.get(username=username)
        username = username + generate_number_random(3)
    except User.DoesNotExist:
        pass

    return username


def str_to_pinyin(chi_characters):
    '''
    获取中文字符串的简拼和全拼字符串
    '''
    if not isinstance(chi_characters, unicode):
        chi_characters = chi_characters.decode('utf-8')

    # 获得昵称的简拼,如 张三：zs
    chi_spell = pypinyin.slug(chi_characters, separator='', style=pypinyin.FIRST_LETTER)
    # 获得昵称的全拼, 张三: zhangsan
    chi_spell_all = pypinyin.slug(chi_characters, separator='')

    return chi_spell, chi_spell_all


def check_emoji(unicode_string):
    #co = re.compile('[\U00010000-\U0010ffff]')
    if unicode_string:
        co = re.search('[\U00010000\-\U0010ffff]', unicode_string)
        #if co.match(unicode_string):
        if co:
            return True
        else:
            return False
    else:
        return False


def is_int(str):
    '''匹配正整数'''
    if re.match("^[0-9]*[1-9][0-9]*$", str.strip()) == None:
        return False
    return True
