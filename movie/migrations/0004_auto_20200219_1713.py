# Generated by Django 2.1.1 on 2020-02-19 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20200215_1610'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='doubanmovie',
            table='movie_top250',
        ),
    ]