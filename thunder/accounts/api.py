# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from rest_framework.decorators import list_route
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.utils import timezone

from .serializers import UserSerializer, LoginSerializer, SignupSerializer
from .models import User, MobileCode
from common.serializers import NoneSerializer
from common.api import APIResponse
import common.utils as utils
from common.decorators import encrypted


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer

    # permission_classes = []

    @list_route(methods=['post'])
    @encrypted()
    def login(self, request, *args, **kwargs):
        '''
        接口描述: 账号登录
        --------------------

        成功返回示例:
        -------------
            {
              "token": {
                "暂不实现token"
              },
              "user": {
                "id": 32255,
                "username": "专门用来造数据账号",
                "chi_spell": "nmm",
                "chi_spell_all": "nimingming",
                "is_active": true,
                "avatar_xs": "/media/avatar/2016/10/21/09/5108/2016_10_21_09_51_06.80x80.jpg",
                "avatar_sm": "/media/avatar/2016/10/21/09/5108/2016_10_21_09_51_06.160x160.jpg",
                "avatar_md": "/media/avatar/2016/10/21/09/5108/2016_10_21_09_51_06.320x320.jpg",
                "avatar_lg": "/media/avatar/2016/10/21/09/5108/2016_10_21_09_51_06.640x640.jpg",
                "description": "",
                "city": "",
                "province": "",
                "gender": null,
                "followed_by_count": 0,
                "friends_count": 2,
                "status_count": 0,
                "symbols_count": 38,
                "portfolios_count": 2,
                "portfolios_following_count": 5,
                "date_joined": "2016-09-05T05:47:30Z",
                "verified": false,
                "verified_type": -1,
                "verified_status": -1,
                "verified_reason": "",
                "mobile": "13700000000"
              }
            }

        错误返回:
        ---------

            =======================  ============================================================
                  error_key                                response
            =======================  ============================================================
                account_not_blank           [账号不能为空]
                password_not_blank          [密码不能为空]
                account_format              [账号需为邮箱/手机号]
                account_unregistered        [账号未注册]
                email_not_active            [Email未激活]
                inactive                    [账号未激活]
                password_not_set            [该账号未设置密码]
                account_invalid             [账号或密码不正确]
            =======================  ============================================================
        '''
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = None
            error_dict = None  # 错误信息
            email = serializer.validated_data.get("email")
            mobile = serializer.validated_data.get("mobile")
            captcha = serializer.validated_data.get("captcha")
            password = serializer.validated_data.get("password")
            username = email or mobile
            # print username
            if not username:
                return APIResponse(errors={'account_not_blank': ['账号不能为空']})

            if not password and not captcha:
                return APIResponse(errors={'password_not_blank': ['必须有密码或验证码']})

            # 验证码校验
            if captcha:
                captcha_key = mobile.strip()
                veryinfo = utils.verify_captcha(captcha_key, captcha)
                if veryinfo <> 0:
                    return APIResponse(errors=veryinfo)

            # 手机号校验
            if mobile:
                if not User.objects.filter(mobile=mobile).exists():
                    if re.match("^%s" % utils.china_mobile_head(), mobile
                                ) and len(mobile) == 11:
                        if not utils.is_mobile(mobile, 1):
                            return APIResponse(errors={'mobile_error': ['手机号格式错误']})
                        else:
                            return APIResponse(
                                errors={'account_unregistered': [
                                    '账号不存在，请重新输入或注册新账号']})
                    return APIResponse(errors={'mobile_error': ['请输入正确账号']})

            try:
                username = username.strip()
                ue = User.objects.get(Q(mobile=username) | Q(email=username))
            except User.DoesNotExist:
                return APIResponse(errors={'account_unregistered': ['账号未注册']})
            # 登录
            if error_dict:
                return APIResponse(errors=error_dict)
            else:
                if password:
                    username = ue.username
                    ue = auth.authenticate(username=username, password=password)
                if ue:
                    auth.login(request, ue)
                else:
                    return APIResponse(errors={'account_invalid': ['账号或密码错误，请重新输入']})
        else:
            return APIResponse(errors=serializer.errors)
        user_info = UserSerializer(ue).data
        user_info['mobile'] = ue.mobile

        return APIResponse({'user': user_info})


class SignupViewSet(viewsets.GenericViewSet):
    throttle_scope = 'critical'
    serializer_class = SignupSerializer

    @list_route(methods=['post'])
    @encrypted()
    def signup(self, request, *args, **kwargs):
        '''
        接口描述：账号注册
        ----------------------------

        成功返回示例:
        -------------
            {
              "is_new_user": true,
              "user": {
                "id": 9,
                "avatar_xs": "",
                "avatar_sm": "",
                "avatar_md": "",
                "avatar_lg": "",
                "last_login": "2019-01-09T08:20:47Z",
                "is_superuser": false,
                "username": "anson2",
                "chi_spell": "anson2",
                "chi_spell_all": "anson2",
                "first_name": "",
                "last_name": "",
                "email": null,
                "password": "pbkdf2_sha256$36000$iT81naTu7voT$BRYz4WP5zswxzi/6B6YjnnEoZe1Bd4Egf0RFRnsF5zU=",
                "is_password_set": true,
                "is_username_set": true,
                "date_joined": "2019-01-09T08:20:47Z",
                "is_staff": false,
                "avatar": null,
                "mobile": "15259227112",
                "province": null,
                "city": null,
                "district": null,
                "street": null,
                "gender": 0,
                "description": null,
                "birthday": null,
                "career": null,
                "qq": null,
                "we_chat": null,
                "we_bo": null,
                "modified_at": "2019-01-09T08:20:47Z",
                "verified_status": -1,
                "verified_reason": null,
                "is_system": false,
                "mobile_code": 1,
                "groups": [],
                "user_permissions": []
              }
            }

        错误返回:
        ------------

            =============================  =========================================================
                  error_key                          response
            =============================  =========================================================
                    inactive                          '账号未激活'
                mobile_unbound              '请下载最新版本并绑定手机号'
                social_unbound              '请下载最新版本并绑定手机号'
                username_not_blank                  '昵称不能为空'
                username_invalid            '昵称长度4-20个字符，支持中英文、数字、-、_'
                username_invalid                   '昵称不能全为数字'
                username_invalid                  '昵称不能全为数字'
                username_invalid                  '昵称不合法'
                username_used                       '昵称不合法'
                username_used                      '该昵称已注册'
                mobile_blank                       '手机号不能为空'
                mobile_registered            '该手机号已注册,请用手机号登录'
                password_blank                     '密码不能为空'
                password_length               '密码6~16个字符，区分大小写'
                password_space                     '密码不能为空'
                     fail                              '注册失败'
                password_invalid                 '密码必须包含“数字、字母、符号”中至少2种元素，密码长度6-16位'
                code_invalid                        '邀请码不存在'
                invite_mobile_not_bind              '邀请人手机号未绑定'
            =============================  =========================================================
        '''
        is_new_user = False
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            mobile = serializer.validated_data.get("mobile")
            captcha = serializer.validated_data.get("captcha")
            captcha = captcha.lower() if captcha else ''
            password = serializer.validated_data.get("password")
            mobile_code_id = serializer.validated_data.get('mobile_code_id')
            invite_code = serializer.validated_data.get("invite_code")
            invite_code = invite_code.lower() if invite_code else ''
            # 如果有验证码, 先验证
            captcha_key = None
            if captcha:
                captcha_key = mobile.strip()
                veryinfo = utils.verify_captcha(captcha_key, captcha)
                if veryinfo != 0:
                    return APIResponse(errors=veryinfo)
            if not captcha:
                return APIResponse(errors={'captcha_not_blank': ['验证码不能为空']})
            # 手机区号默认为中国大陆
            if not mobile_code_id:
                mobile_code_id = 1
            try:
                mobile_code = MobileCode.objects.get(pk=mobile_code_id)
            except MobileCode.DoesNotExist:
                return APIResponse(errors={'mobile_code_not_exist': ['手机区号不存在']})
            # 手机账号判断
            if not mobile:
                return APIResponse(errors={'mobile_blank': ['手机号不能为空']})
            else:
                if not utils.is_mobile(mobile, mobile_code.id):
                    return APIResponse(errors={'mobile_error': ['手机号格式错误']})
                try:
                    User.objects.get(mobile=mobile)
                    return APIResponse(errors={'mobile_registered': ['该手机号已注册']})
                except User.DoesNotExist:
                    captcha_key = mobile.strip()
            invite_code_key = None
            # 邀请码校验
            if invite_code:
                invite_code_key = mobile.strip()
                private = utils.private_invite_code(invite_code_key, invite_code)
                if private != 0:
                    return APIResponse(errors=private)
            if not invite_code:
                return APIResponse(errors={'captcha_not_blank': ['邀请码不能为空']})
            username, is_username_set = self._check_username(username)
            with transaction.atomic():
                user, is_new_user = self._create_new_user(
                    username, mobile, password,
                    is_username_set, mobile_code)
                if not user and not is_new_user:
                    return APIResponse(errors={'user_already': ['用户已注册成功']})

                login_user = auth.authenticate(username=username, password=password)
                auth.login(request, login_user)
                datas = self._login_user_info(
                    request, user, is_new_user, captcha_key)
            return APIResponse(datas)
        else:
            return APIResponse(errors=serializer.errors)

    def _login_user_info(self, request, user, is_new_user, captcha_key):
        '''
        登入用户信息
        '''
        user_info = UserSerializer(user).data
        user_info['mobile'] = user.mobile

        # 释放验证码
        # if conn.exists(captcha_key):
        #     conn.delete(captcha_key)

        return {'user': user_info, 'is_new_user': is_new_user}

    def _create_new_user(
            self, username, mobile, password, is_username_set, mobile_code):
        '''
        创建新用户
        '''
        chi_spell, chi_spell_all = utils.str_to_pinyin(username.strip())
        try:
            user, created = User.objects.get_or_create(mobile=mobile, defaults={
                'username': username.strip(),
                'chi_spell': chi_spell,
                'chi_spell_all': chi_spell_all,
                'mobile_code': mobile_code,
                'is_username_set': is_username_set,
                'last_login': timezone.now()
            })
        except IntegrityError:
            return None, False
        if not created:
            return user, False
        if password:
            user.set_password(password)
            user.is_password_set = True
        else:
            user.is_password_set = False
        user.save(update_fields=['password', 'is_password_set'])
        is_new_user = True
        return user, is_new_user

    def _check_username(self, username):
        is_username_set = True
        # utf8一个汉字占3个字节，gbk一个汉字占2个字节

        username = unicode(username.strip()) if username else ''
        # 昵称未填写
        if not username:
            username = utils.generate_username('')
            is_username_set = False

        else:
            # 昵称长度判断
            if not utils.is_right_string(username) or \
                    (len(username.strip().encode('gbk')) < 4 or \
                     len(username.strip().encode('gbk')) > 20):
                return APIResponse(
                    errors={
                        'username_invalid': ['昵称长度4-20个字符，支持中英文、数字、-、_']
                    })

            # 检查昵称是否全为数字
            if re.match("^[0-9]+$", username):
                return APIResponse(errors={"username_invalid": ['昵称不能全为数字']})

        # # 检查昵称是否有敏感词
        # if illegal_words_check.contains_illegal_words(username):
        #     return APIResponse(errors={"username_invalid": ['昵称不合法']})
        #
        # # 手机注册用户的昵称判断
        # else:
        #     username_used = utils.verify_usernamge(username)
        #     if username_used:
        #         return APIResponse(errors=username_used)

        return username, is_username_set


class LogoutViewSet(viewsets.GenericViewSet):
    serializer_class = NoneSerializer
    permission_classes = [IsAuthenticated]

    @list_route(methods=['get'])
    def logout(self, request, *args, **kwargs):
        '''
        接口描述：退出登录
        ----------------------------

        成功返回示例:
        -------------
            {
              "status": True
            }

        错误返回:
        ------------

            =============================  =========================================================
                  error_key                          response
            =============================  =========================================================

            =============================  =========================================================
        '''
        auth.logout(request)
        return APIResponse({'status': True})

