from django.db import models

# Create your models here.


class DouBanMovie(models.Model):
    name = models.CharField(max_length=30, verbose_name='影视名')
    pub_time = models.CharField(max_length=6, verbose_name='上映年份')
    pic_url = models.CharField(max_length=100, verbose_name='海报链接')
    detail_url = models.CharField(max_length=50, verbose_name='豆瓣链接')
    director = models.CharField(max_length=30, verbose_name='导演')
    star = models.CharField(max_length=10, verbose_name='豆瓣评分')
    evaluate_num = models.CharField(max_length=10, verbose_name='评价人数')
    quote = models.CharField(max_length=50, verbose_name='电影名言')
    detail_title = models.CharField(max_length=100, verbose_name='详细标题')
    introduce = models.CharField(max_length=1000, verbose_name='电影简介')
    detail = models.CharField(max_length=1000, verbose_name='电影详情')
    type = models.CharField(max_length=30, default="豆瓣top250", verbose_name='类型')
    play_url = models.CharField(max_length=500, default='暂无', verbose_name="电影资源链接")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "movie_top250"
        verbose_name = '豆瓣Top250'
        verbose_name_plural = '豆瓣Top250'


class Movie(models.Model):
    name = models.CharField(max_length=30, verbose_name='影视名')
    type = models.CharField(max_length=10, verbose_name='类型')
    pub_time = models.CharField(max_length=6, verbose_name='上映年份')
    pic_url = models.CharField(max_length=100, verbose_name='海报链接')
    detail_url = models.CharField(max_length=50, verbose_name='豆瓣链接')
    director = models.CharField(max_length=30, verbose_name='导演')
    star = models.CharField(max_length=10, verbose_name='豆瓣评分')
    evaluate_num = models.CharField(max_length=10, verbose_name='评价人数')
    detail_title = models.CharField(max_length=100, verbose_name='详细标题')
    introduce = models.CharField(max_length=1000, verbose_name='电影简介')
    detail = models.CharField(max_length=1000, verbose_name='电影详情')
    # 区分电影还是电视
    classify = models.CharField(max_length=10, default='movie', verbose_name='电影或电视')
    play_url = models.CharField(max_length=500, default='暂无', verbose_name="电影资源链接")

    def classify_name(self):
        if self.classify == 'movie':
            return '电影'
        else:
            return '电视'
    # 设置排序依据字段
    classify_name.admin_order_field = 'classify'
    # 设置函数显示的中文名
    classify_name.short_description = '电影或电视'

    def __str__(self):
        return self.name

    class Meta:
        db_table = "movie_tv"
        verbose_name = '电影_电视'
        verbose_name_plural = '电影__电视'
