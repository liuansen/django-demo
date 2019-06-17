# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from accounts import api
from thunder.router import router


router.register(r'account', api.SignupViewSet, 'accounts_signup')
router.register(r'account', api.LoginViewSet, 'accounts_login')
router.register(r'accounts', api.LogoutViewSet, 'accounts_logout')


urlpatterns = [
]
