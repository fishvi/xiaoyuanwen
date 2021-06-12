from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    pass


admin.site.site_header = '校园问后台管理系统'
admin.site.site_title = '后台管理系统 | 管理员'
