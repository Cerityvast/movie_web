from django.urls import path, re_path
from movie import views

urlpatterns = [
    path('index', views.index),         # 进入主页
    re_path(r'movie_detail/(\d*)', views.movie_detail),         # 电影详情
    path('play', views.play_movie),         # 观看电影
    re_path(r'movie_type/(?P<page>\d*)', views.movie_type),          # 电影类型列表
    path('tv_type', views.tv_type),          # 电视类型列表
    path('new_publish', views.new_publish),         # 最新上映
    path('search_list', views.search_list),         # 搜索电影列表
    re_path(r'search', views.search),   # 获取查询后的结果
]
