# Generated by Django 2.0 on 2020-02-14 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DouBanMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('pic_url', models.CharField(max_length=100)),
                ('detail_url', models.CharField(max_length=50)),
                ('director', models.CharField(max_length=30)),
                ('star', models.CharField(max_length=10)),
                ('evaluate_num', models.CharField(max_length=10)),
                ('quote', models.CharField(max_length=50)),
                ('detail_title', models.CharField(max_length=100)),
                ('introduce', models.CharField(max_length=1000)),
                ('detail', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'movie',
            },
        ),
    ]