# Generated by Django 2.2.1 on 2020-11-09 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='medstore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='药店用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('ypjyxkzcode', models.CharField(max_length=9, verbose_name='药品经营许可证号码')),
                ('gspcode', models.CharField(max_length=13, verbose_name='gsp证书编号')),
                ('name', models.CharField(max_length=20, verbose_name='药店名称')),
                ('desc', models.CharField(max_length=256, verbose_name='药店简介')),
                ('address', models.CharField(max_length=40, verbose_name='药店地址')),
                ('postcode', models.CharField(max_length=20, verbose_name='邮政编码')),
                ('time', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]
