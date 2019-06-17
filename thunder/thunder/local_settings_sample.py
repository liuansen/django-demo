# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '3306',
    }
}

CLIENT_PUBLIC_KEY = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCujEBWcC8uTvb3w8HSOVxJ5ldZAGVXqay1FuZaiaQh1AD5hbSulwLGGqV9' \
                    'zI1dL936SBgJJu1fA2wKO6Ssn9DVx+z5IKIte3ZzjXbtbE8wqn6Qti/ccD6MRROO/Dt0ceBWCDfIh3YKSU2OEFnvP8+bD7' \
                    'u1nu1AUzj7z44yDPSVwQIDAQAB'
SERVER_PRIVATE_KEY = 'MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAJYYtd8Nv1Km3CKnhRJoA8ghCEk4/yln6mXY3fHk/CBZ77d' \
                     '3iONZG9g/33tgwd6HsGdF6j3n3KEiRypFY3liqyWHOS+6W+AFaTd9XztNcqL2KzM6qDsNzSMGop4kzEpwZnSDUZkcxi2Pr' \
                     'yNGquz+F/C5R7fxSgO4JUVov3uo9aIHAgMBAAECgYBRKX9+48InAU9b9dXBRDl3SFVgss9XJnfbJs+s87NaEwfK33pH5XF' \
                     'nF/LSlll+6UR8M5QccXoeL5jnxKmrg60jQyLX/WsTEw1U2JKVDX49fmDwXnz0B4Msikq2CFIqjksHPaZD9Suyaj41pz4s' \
                     '5LQ0iyMVZFHO3+FZw3oiZm5O0QJBANU65icwEiEAQghL+aNQYefv208ki8ycEi+t7+z4iCxkb5IcWzbCtRi1U3+ggFBkqB' \
                     'SaDwvlIqDLtmB4crBmn20CQQC0M/tLhFYtVuKpVkDl95UuM5vFVXZih0Z1jelF6Y3f7mNeMOkJT9vhWair3Z76svFElsVK' \
                     'TZSxlACkwxHsqbrDAkBpyyNN5ifYf8xDWY6uXL922CaziapjBjxvs5kKtfS6Mcq5b6BB9zDq5WxcMkH3oTlTn2w/tpwLs4' \
                     'b1Lk2ZABGxAkAdpYesTuNWpjq4HUakDu1uInN4La1CXHsNEAHWzKvYsYGLl4RfUdIc6wFC9T0YhaQH4r4mkUjrRiws7yLdy' \
                     'ra9AkAHTmtbXW3r7SE/j5+tGVAmJKVCRLzJvo+i6jeC4Hxf7evKATR/IK023pibjKXoOdLTUeZeclrrzVvYjp31AF52'
