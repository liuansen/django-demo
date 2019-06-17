# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from accounts.models import User


class Platform(models.Model):
    """
    自媒体平台
    """
    user = models.ForeignKey(User, verbose_name='用户')
    PLATFORM_TYPE = (
        (-1, '无'),
        (0, '微信公众号'),
        (1, '百度百家号'),
        (2, '今日头条号'),
        (3, '新浪微博平台'),
        (4, 'qq新闻'),
        (5, '网易号平台'),
        (6, '阿里UC平台'),
        (7, '抖音平台'),
        (8, '知乎'),
    )
    platform_type = models.SmallIntegerField('平台名称', null=True, blank=True, choices=PLATFORM_TYPE, default=-1)
    platform_username = models.CharField('平台账号', blank=True, null=True, max_length=100)
    platform_password = models.CharField('平台密码', blank=True, null=True, max_length=100)
    platform_nickname = models.CharField('平台账号昵称', blank=True, null=True, max_length=100)
    platform_openid = models.CharField('平台openid', blank=True, null=True, max_length=300)
    platform_appid = models.CharField('平台appid', blank=True, null=True, max_length=300)
    fans_count = models.IntegerField('关注数', null=True, blank=True, default=0)
    date_joined = models.DateField('注册时间', default=timezone.now)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    modified_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '自媒体平台'
        verbose_name_plural = verbose_name


class Content(models.Model):
    """
    文章管理
    """
    CONTENT_TYPE = (
        (0, '无'),
        (1, '旅游攻略'),
        (2, '娱乐资讯'),
        (3, '游戏攻略'),
        (4, '购物折扣'),
        (5, '金融开户'),
        (6, '美食攻略'),
        (7, '其他'),
    )
    content_type = models.SmallIntegerField('文章类型', null=True, blank=True, choices=CONTENT_TYPE, default=0)
    platform = models.ForeignKey(Platform, verbose_name='自媒体平台')
    title = models.CharField('文章标题', null=True, blank=True,  max_length=200)
    auth = models.CharField('作者', null=True, blank=True, max_length=100)
    text = models.TextField('正文', help_text="正文")
    is_crawl = models.BooleanField('是否是爬取的文章', default=False)
    crawl_date = models.DateField('爬取时间', default=timezone.now)
    is_release = models.BooleanField('是否发布', default=False)
    release_date = models.DateField('发布时间', default=timezone.now)
    retweets_count = models.PositiveIntegerField('转发数', default=0, help_text='转发数', editable=False)
    comments_count = models.PositiveIntegerField('回复数', default=0, help_text='回复数', editable=False)
    attitudes_count = models.PositiveIntegerField('赞数', default=0, help_text='赞数', editable=False)
    favorites_count = models.PositiveIntegerField('收藏数', default=0, help_text='收藏数', editable=False)
    views_count = models.PositiveIntegerField('阅读数', default=0, help_text='阅读数', editable=False)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    modified_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name
