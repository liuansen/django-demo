# coding=utf-8
from django.contrib import admin
from django.contrib.auth import get_permission_codename


class CustomModelAdmin(admin.ModelAdmin):
    '''
    readonly权限，与add／delete／change权限相斥，忌共存
    '''
    def has_view_permission(self, request, obj=None):
        '''
        判断只读权限方法
        '''
        opts = self.opts
        codename = get_permission_codename('view', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def get_model_perms(self, request):
        '''
        对应权限model列表获取
        '''
        value = super(CustomModelAdmin, self).get_model_perms(request)
        value['view'] = self.has_view_permission(request)
        return value

    def has_change_permission(self, request, obj=None):
        '''
        想能view，change_permission置为True
        '''
        change = super(CustomModelAdmin, self).has_change_permission(request)
        return self.has_view_permission(request) or change

    def get_readonly_fields(self, request, obj=None):
        '''
        页面只读
        '''
        if not request.user.is_superuser and self.has_view_permission(request) == True:
            self.save_on_top = False
            self.change_form_template = "admin/view_readonly.html"
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields

    def get_actions(self, request):
        '''
        只读view actions的选项去除
        '''
        actions = super(CustomModelAdmin, self).get_actions(request)
        if not request.user.is_superuser and self.has_view_permission(request) == True:
            if actions.has_key('delete_selected'):
                del actions["delete_selected"]
            return actions
        return actions
