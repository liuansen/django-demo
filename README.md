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
