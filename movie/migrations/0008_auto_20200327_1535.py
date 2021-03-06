# Generated by Django 2.0 on 2020-03-27 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_doubanmovie_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doubanmovie',
            options={'verbose_name': '豆瓣Top250', 'verbose_name_plural': '豆瓣Top250'},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'verbose_name': '电影_电视', 'verbose_name_plural': '电影__电视'},
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='detail',
            field=models.CharField(max_length=1000, verbose_name='电影详情'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='detail_title',
            field=models.CharField(max_length=100, verbose_name='详细标题'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='detail_url',
            field=models.CharField(max_length=50, verbose_name='豆瓣链接'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='director',
            field=models.CharField(max_length=30, verbose_name='导演'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='evaluate_num',
            field=models.CharField(max_length=10, verbose_name='评价人数'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='introduce',
            field=models.CharField(max_length=1000, verbose_name='电影简介'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='name',
            field=models.CharField(max_length=30, verbose_name='影视名'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='pic_url',
            field=models.CharField(max_length=100, verbose_name='海报链接'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='pub_time',
            field=models.CharField(max_length=6, verbose_name='上映年份'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='quote',
            field=models.CharField(max_length=50, verbose_name='电影名言'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='star',
            field=models.CharField(max_length=10, verbose_name='豆瓣评分'),
        ),
        migrations.AlterField(
            model_name='doubanmovie',
            name='type',
            field=models.CharField(default='豆瓣top250', max_length=30, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='classify',
            field=models.CharField(default='movie', max_length=10, verbose_name='电影或电视'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='detail',
            field=models.CharField(max_length=1000, verbose_name='电影详情'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='detail_title',
            field=models.CharField(max_length=100, verbose_name='详细标题'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='detail_url',
            field=models.CharField(max_length=50, verbose_name='豆瓣链接'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(max_length=30, verbose_name='导演'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='evaluate_num',
            field=models.CharField(max_length=10, verbose_name='评价人数'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='introduce',
            field=models.CharField(max_length=1000, verbose_name='电影简介'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=30, verbose_name='影视名'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='pic_url',
            field=models.CharField(max_length=100, verbose_name='海报链接'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='pub_time',
            field=models.CharField(max_length=6, verbose_name='上映年份'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='star',
            field=models.CharField(max_length=10, verbose_name='豆瓣评分'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='type',
            field=models.CharField(max_length=10, verbose_name='类型'),
        ),
    ]
