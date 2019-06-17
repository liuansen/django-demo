Welcome to django_demo!
===================

# 下载代码后进入django_demo/xenv
    1.运行virtualenv thunder
    2.source thunder/bin/activate
    3.cd 到根目录执行：pip install -r requirements.txt
    4.cd 到package/django-mobile-master目录执行 python setup.py install

# 进入thunder项目的thunder目录thunder/thunder
    1.拷贝local_settings_sample.拷贝local_settings.py
    2.填写本地的MySQL地址
    3.这里提供一个网上的MySQL的地址，但是速度会比较慢
        host: db4free.net
        name: django_demp
        user: tywq_django
        password: 962464

# 启动项目,进入thunder项目根目录thunder/：
    1.如果使用本地MySQL才需要执行以下操作
        i1. 执行python manage.py migrate
        i2. 执行python manage.py createsuperuser 按照提示输入创建超级用户
        i3. 执行python manage.py runserver启动项目

# 查看api地址：
    在浏览器输入127.0.0.1:8000/docs

# work
    1.get /accounts/user_info  查看用户基本信息，接口返回数据如下
    '''
        接口描述: 查看用户基本信息
        ------------------------------

        成功返回示例:
        -------------

            {
              "id": 1,用户ID,int
              "username": "张三", #昵称
              "chi_spell": "zs", #拼音简称
              "chi_spell_all": "zhangsan"， #拼音全称
              "is_active": true,
              "avatar_xs": "/media/avatar/2014/08/07/10/0552/n.80x80.jpg",80x80头像地址,string
              "avatar_sm": "/media/avatar/2014/08/07/10/0552/n.160x160.jpg",160x160头像地址,string
              "avatar_md": "/media/avatar/2014/08/07/10/0552/n.320x320.jpg",320x320头像地址,string
              "avatar_lg": "/media/avatar/2014/08/07/10/0552/n.640x640.jpg",640x640头像地址,string
              "description": "I am superuser",简介,string
              "city": "浦东",城市,string
              "province": "上海",省份,string
              "gender": 1,(0: '保密',1: '男',2: '女')
              "category": [
                3
              ],
              "followed_by_count": 0,粉丝数,int
              "friends_count": 0,关注数,int
              "status_count": 0,帖子数,int
              "symbols_count": 1,自选股数量,int
              "portfolios_count": 0,自建组合数量,int
              "portfolios_following_count": 0,自选组合数量,int
              "is_self": false, 是否是当前登陆用户
              "me_follow": false, 是否关注过他
              "date_joined": "2014-06-14T22:12:54Z",用户注册时间
              "verified": true, #是否认证用户
              "verified_type": 1, #认证类型 -1,未认证 0, 投资牛人 1, 投资顾问 2, 分析师 3, 基金执业 4, 期货执业
              "verified_status": 1, #认证审核状态 -1,未提交 0, '审核中' 1, '已认证' 2, '审核失败'
              "verified_reason": "兴业证券 投资顾问 aaa", #认证原因
            }

        错误返回:
        ---------

            =======================  ============================================================
                  error_key                                response
            =======================  ============================================================
                    pk_invalid          pk必须是整数型
                    user_invalid        用户不存在！
            =======================  ============================================================

        '''
    2. GET /api/v1/we_media/ 接口描述: 用户管理平台列表
    '''
        接口描述: 创建自媒体平台
        ------------------------------

        成功返回示例:
        -------------
            {
              "platform_type": 3,   # 自媒体编号
              "platform_username": "ksksksk",  # 自媒体平台账号
              "platform_password": "1231321",  # 平台密码
              "platform_openid": "afsadfsdf",  # 平台openid
              "platform_appid": "213a2s",      # 平台appid
              "date_joined": "2018-12-01"      # 注册时间
            }

        错误返回:
        ---------

            =======================         ============================================================
                  error_key                             response
            =======================         ============================================================
                params_error                        参数错误
                verified_status_invalid             用户未认证，无法创建
                platform_exist                      自媒体平台已存在, 请重新输入
            =======================         ============================================================
        '''

    3. POST /api/v1/we_media/ 接口描述: 创建自媒体平台
    '''
        接口描述: 用户管理平台列表
        ------------------------------

        成功返回示例:
        -------------
            {
              "total_count": 1,
              "total_page": 1,
              "current_page": 1,
              "results": [
                {
                  "id": 1,   # id
                  "user": 2,   # 用户id
                  "platform_type": 0,
                  "platform_type_display": "微信公众号"   # 平台类型
                }
              ]
            }

        错误返回:
        ---------

            =======================  ============================================================
                  error_key                          response
            =======================  ============================================================
                    params_error          参数错误
            =======================  ============================================================
        platform_type -- 平台类型
        '''

    4. GET /api/v1/we_media/list_of/ 接口描述: 平台类型
    '''
         接口描述: 平台类型
        ------------------------------

        成功返回示例:
        -------------
            [
              {
                "title": "知乎",
                "iocn": 8
              }
            ]

        错误返回:
        ---------

            =======================  ============================================================
                  error_key                                response
            =======================  ============================================================
                    pk_invalid              pk必须是整数型
                    platform_invalid        平台不存在！
            =======================  ============================================================
        '''

    5. GET /api/v1/we_media/{pk}/ 接口描述: 查看用户管理的平台基本信息
    '''
        接口描述: 查看用户管理的平台基本信息
        ------------------------------

        成功返回示例:
        -------------

            {
              "id": 1,
              "user": 2,  # 用户id
              "username": "root",  # 用户昵称
              "platform_type": 0,
              "platform_type_display": "微信公众号",   # 平台类型
              "platform_username": "anson",   # 平台账号
              "platform_password": "zxc12345",   # 平台密码
              "platform_openid": "hfhsdjfhsajdfhjhds",   #　平台ｏｐｅｎｉｄ
              "platform_appid": "sdjaksjdajsd",　　　# 平台appid
              "fans_count": 1000000,   # 关注数
              "date_joined": "2019-01-08",   # 注册时间
              "created_at": "2019-01-08T02:59:32Z",  # 创建时间
              "modified_at": "2019-01-08T02:59:32Z"  # 修改时间
            }

        错误返回:
        ---------

            =======================  ============================================================
                  error_key                                response
            =======================  ============================================================
                    pk_invalid              pk必须是整数型
                    platform_invalid        平台不存在！
                    user_invalid            不是您的平台无权查看
            =======================  ============================================================
        '''