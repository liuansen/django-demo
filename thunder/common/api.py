# -*- coding:utf8 -*-

from rest_framework import status
from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, data={'status': True}, errors=None, http_status=status.HTTP_200_OK):
        resp = {"errors": errors} if errors else data
        super(APIResponse, self).__init__(
            resp, http_status
        )



'''
from collections import namedtuple

Status = namedtuple('Status', 'code msg')

DONE_200_OK = Status(200, u"成功")

CLIENT_400_PARAMETER_ERROR = Status(400, u"参数错误")

CLIENT_401_PASSWORD_ERROR = Status(401, u"密码错误")

SERVER_500_DATABASE_CONNECT_LOST = Status(500, u"数据库连接失败")
def get_status_document():
    ret = {}
    for status in dir(api_status):
        s = getattr(api_status,status)
        if isinstance(s, api_status.Status):
            ret[status]=(s.code, s.msg)
    return ret

'''