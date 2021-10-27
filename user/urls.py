from django.urls import path, re_path
from user import views

urlpatterns = [
    path('register', views.register),               # 用户注册
    path('confirm', views.user_confirm),            # 用户注册验证
    path('login', views.login),                     # 用户登录
    path('logout', views.logout),                   # 用户注销
    path('personal_index', views.personal_index),   # 个人中心
    path('personal_info', views.personal_info),     # 个人信息修改界面
    path(r'personal_history', views.personal_history),    # 个人历史记录
    re_path(r'delete_history/(\d+)', views.delete_history),  # 删除指定历史记录
    path('modify_info', views.modify_info),          # 修改用户密码
    path(r'show_evaluate', views.show_evaluate),    # 显示电影评分列表
    path('mark_movie', views.mark_movie),           # 对电影进行评分
    path('recommend_movie', views.recommend_movie),     # 显示推荐电影
    path('comment_movie', views.comment_movie),     # 用户评价电影
]
