from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名')
    password = models.CharField(max_length=30, verbose_name='密码')
    sex = models.CharField(max_length=5, verbose_name='性别')
    age = models.CharField(max_length=3, verbose_name='年龄')
    email = models.CharField(max_length=30, verbose_name='邮箱')
    is_checked = models.CharField(max_length=1, default=0, verbose_name='注册状态(0:未激活 1:已注册)')

    def status(self):
        if self.is_checked == 0:
            return '未激活'
        else:
            return '已注册'
    status.admin_order_field = 'is_checked'
    status.short_description = '注册状态'

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class History(models.Model):
    username = models.CharField(max_length=30)
    video_id = models.CharField(max_length=10)
    current_time = models.CharField(max_length=30)
    # 区分是豆瓣top250的影片还是普通类型影片，0代表top250, 1代表普通影视
    tag = models.CharField(max_length=1)
    # 用户对已观看电影的评分
    evaluate_star = models.CharField(max_length=10)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "history"


# 验证码类---和用户一一对应
class ConfirmString(models.Model):
    """
   确认code类
   """
    code = models.CharField(max_length=256, verbose_name='验证码')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户id')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='当前验证时间')

    def username(self):
        return self.user.username

    def __str__(self):
        return self.user.name + ': ' + self.code

    class Meta:
        db_table = "user_confirm_code"
        verbose_name = '注册状态表'
        verbose_name_plural = '注册状态表'


# 用户评论类
class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=10)
    # 区分是豆瓣top250的影片还是普通类型影片，0代表top250, 1代表普通影视
    tag = models.CharField(max_length=1, default=0)
    comment = models.CharField(max_length=300)
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "UserComment"
