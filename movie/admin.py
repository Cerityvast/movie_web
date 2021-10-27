from django.contrib import admin
from movie.models import DouBanMovie, Movie


class DouBanMovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'director', 'pub_time', 'star', 'evaluate_num']  # 显示相关列
    list_per_page = 30  # 每页显示30部影片
    list_filter = ['pub_time']  # 列表页右侧过滤栏
    search_fields = ['name', 'director', 'pub_time']  # 列表页上方的搜索框
    fieldsets = (
        ('点影基本信息', {'fields': ['name', 'director', 'pub_time']}),
        ('点影详情', {'fields': ['detail_title', 'pic_url', 'detail_url',
                             'star', 'evaluate_num', 'quote', 'introduce', 'detail']})
    )


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'director', 'pub_time', 'classify_name', 'star', 'evaluate_num']  # 显示相关列
    list_per_page = 30  # 每页显示30部影片
    list_filter = ['type']  # 列表页右侧过滤栏
    search_fields = ['name', 'director', 'pub_time']  # 列表页上方的搜索框
    fieldsets = (
        ('影视基本信息', {'fields': ['name', 'type', 'director', 'pub_time', 'classify']}),
        ('影视详情', {'fields': ['detail_title', 'pic_url', 'detail_url',
                             'star', 'evaluate_num', 'introduce', 'detail']})
    )


admin.site.register(DouBanMovie, DouBanMovieAdmin)
admin.site.register(Movie, MovieAdmin)
