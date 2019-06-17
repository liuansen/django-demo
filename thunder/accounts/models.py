# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import validators
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.

from common.thumbs import ImageWithThumbsField


class MobileCode(models.Model):
    '''
    手机的国家\地区区号
    '''
    code = models.CharField('手机的国家\地区区号', max_length=10, help_text='手机的国家\地区区号')
    zone = models.CharField('国家\地区', max_length=30, help_text='国家\地区')
    min_digit = models.PositiveIntegerField(default=0)
    max_digit = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.zone

    class Meta:
        verbose_name = '手机的国家\地区区号'
        verbose_name_plural = '手机的国家\地区区号'


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        '昵称', max_length=30, unique=True, help_text='昵称长度4-20个字符，支持中英文、数字、-、_',
        validators=[
            validators.RegexValidator('^[a-zA-Z0-9-_\u4e00-\u9fa5]+$',
                                      '昵称长度4-20个字符，支持中英文、数字、-、_', 'invalid')
        ])
    chi_spell = models.CharField(max_length=30, blank=True, null=True, verbose_name='昵称中文拼音简称')
    chi_spell_all = models.CharField(max_length=100, blank=True, null=True, verbose_name='昵称中文拼音全拼')
    first_name = models.CharField('昵称首字', max_length=30, blank=True)
    last_name = models.CharField('昵称尾字', max_length=30, blank=True)
    email = models.EmailField('邮箱', default=None, unique=True, null=True, blank=True)
    password = models.CharField('密码', blank=True, null=True, max_length=128)
    is_password_set = models.BooleanField('是否设置密码', default=True,
                                          help_text=_('true：设置密码，false：随机密码(手机验证码注册时随机生成)'))
    is_username_set = models.BooleanField('是否设置昵称', default=True,
                                          help_text=_('true：设置昵称，false：随机昵称(手机验证码注册时随机生成)'))

    date_joined = models.DateTimeField('注册时间', default=timezone.now)
    is_staff = models.BooleanField('是否是职员', default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))

    avatar = ImageWithThumbsField('头像', max_length=800, blank=True, null=True,
                                  upload_to='avatar/%Y/%m/%d/%H/%M%S',
                                  sizes=((80, 80), (160, 160), (320, 320), (640, 640), ))
    mobile = models.CharField('手机号', max_length=100, default=None, unique=True, null=True)
    mobile_code = models.ForeignKey(MobileCode, related_name='zone_user',
                                    null=True, blank=True, default=None, verbose_name='手机区号',
                                    on_delete=models.CASCADE)
    province = models.CharField('省份', max_length=100, null=True, blank=True, db_index=True)
    city = models.CharField('城市', max_length=100, null=True, blank=True, db_index=True)
    district = models.CharField('地区', max_length=50, null=True, blank=True)
    street = models.CharField('详细地址', max_length=100, null=True, blank=True)
    GENDER = (
        (0, '保密'),
        (1, '男'),
        (2, '女'),
    )
    CAREER = (
        ('5', '房地产'),
        ('10', '国有企业'),
        ('2', '教科文'),
        ('3', '金融'),
        ('4', '商贸'),
        ('9', '事业单位'),
        ('1', '政府部门'),
        ('6', '制造业'),
        ('7', '自由职业'),
        ('8', '其他'),
    )
    gender = models.SmallIntegerField('性别', null=True, blank=True, choices=GENDER, default=0)
    description = models.TextField('简介', null=True, blank=True)
    birthday = models.DateField('生日', null=True, blank=True)
    career = models.CharField(
        '职业', choices=CAREER, max_length=20, null=True, blank=True)
    qq = models.CharField(max_length=20, default=None, null=True, blank=True)
    we_chat = models.CharField(
        '微信', max_length=200, default=None, null=True, blank=True)
    we_bo = models.CharField(
        '微博', max_length=200, default=None, null=True, blank=True)

    modified_at = models.DateTimeField('修改时间', auto_now = True)

    VERIFIED_STATUS = (
        (-1, '未提交'),
        (0, '审核中'),
        (1, '已认证'),
        (2, '审核失败'),
    )
    verified_status = models.SmallIntegerField('认证状态', choices=VERIFIED_STATUS, default=-1)
    verified_reason = models.CharField('认证说明', max_length=200, null=True, blank=True)

    is_system = models.BooleanField('是否系统用户', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

        permissions = (
         ("view_user", "用户的只读权限"),
        )

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    '''
    如果用户未设定过密码，则给他设定一个6位数的随机密码，设定成功返回True否则False
    '''
