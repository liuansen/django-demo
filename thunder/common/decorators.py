# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from datetime import datetime, timedelta

from django.conf import settings
from django.http import QueryDict
from django.core.serializers.json import DjangoJSONEncoder

from .encrypt_decrypt import EncryptDecryptAPI
from .api import APIResponse

def singleton(cls, *args, **kw):
    '''
    单例模式 使用装饰器(decorator)
    '''
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

def encrypted(required=False):
    '''
    请求／响应支持加密解密
    required: True 强制必须加密 False 加密可选
    '''
    def decorator(func):
        def handler(self, request, *args, **kwargs):
            data_encrypted = (('data' in request.data and 'signature' in request.data) or 
                ('data' in request.query_params and 'signature' in request.query_params))
            need_encrypt = (settings.ENABLE_ENCRYPTION and 
                not (not data_encrypted and not required))
            if need_encrypt:
                client = EncryptDecryptAPI()                   
                is_post = False
                if 'data' in request.data and 'signature' in request.data:
                    data = request.data.get('data')
                    signature = request.data.get('signature')
                    is_post = True
                elif 'data' in request.query_params and 'signature' in request.query_params:
                    data = request.query_params.get('data')
                    signature = request.query_params.get('signature')
                else:
                    return APIResponse(errors={'request_invalid': ['数据和签名获取失败，非法请求，请重试!']})

                #调用解密函数进行数据解密
                decrypt_data = client.decrypt(json.dumps({'data': data, 'signature': signature})) 

                if not decrypt_data:
                    return APIResponse(errors={'request_invalid': ['数据加解密失败，非法请求，请重试!']})

                try:
                    received_data = json.loads(decrypt_data)
                except ValueError:
                    return APIResponse(errors={'request_invalid': ['数据格式错误，非法请求，请重试!']})
                
                # 时间比较，验证请求时间间隔
                #try:
                #    timestamp = received_data['timestamp']
                #except KeyError:
                #    return APIResponse(errors={'request_invalid': ['数据请求时间有误，非法请求，请重试!']})
                
                #try:
                #    compare_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ") 
                #except ValueError:
                #    return APIResponse(errors={'request_invalid': ['数据请求时间有误，非法请求，请重试!']})

                #访问时间超过20秒，或者客户端当前时间比系统时间提前20秒以上
                #if compare_time < datetime.utcnow() + timedelta(seconds=-20) or compare_time > datetime.utcnow() + timedelta(seconds=20):
                #    return APIResponse(errors={'request_invalid': ['您的系统时间设置不正确， 导致无法建立安全连接， 请正确设置系统时间!']})

                #验证签名正确与否
                check_sign = client.checksign(received_data)
                if not check_sign:
                    return APIResponse(errors={'request_invalid': ['请求无效，请重试！']})
                received_data.pop('timestamp')

                get_mutable = request._request.GET._mutable
                request._request.GET._mutable = True
                if is_post:
                    if isinstance(request.data, QueryDict):
                        post_mutable = request.data._mutable
                        request.data._mutable = True
                #将解密后的明文写入request
                for k in received_data:
                    if is_post:
                        request.data[k] = received_data[k].decode('utf-8')
                    else:
                        request.query_params[k] = received_data[k]
                request._request.GET._mutable = get_mutable
                if is_post:
                    if isinstance(request.data, QueryDict):
                        request.data._mutable = post_mutable

            response = func(self, request, *args, **kwargs)

            if need_encrypt:
                response_data = {"result": json.dumps(response.data, cls=DjangoJSONEncoder), "timestamp": datetime.utcnow().isoformat()}
                response.data = client.encrypt(response_data)

            return response
        handler.__name__ = func.__name__
        return handler

    return decorator