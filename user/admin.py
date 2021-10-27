from django.contrib import admin
from user.models import User, ConfirmString


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'age', 'email', 'sex', 'status']  # 显示相关列
    list_per_page = 30          # 每页显示30个用户
    list_filter = ['sex']  # 列表页右侧过滤栏
    search_fields = ['username']    # 列表页上方的搜索框


admin.site.register(User, UserAdmin)
admin.site.site_header = '电影网站管理'
admin.site.site_title = '登录电影后台管理'
admin.site.index_title = '后台管理'
