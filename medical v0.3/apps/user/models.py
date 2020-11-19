from django.db import models

class User(models.Model):

    username = models.CharField(max_length=32, verbose_name='顾客用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    name = models.CharField(max_length=32,verbose_name='微信昵称')
    phonenumber = models.ImageField(max_length=11, verbose_name='联系方式')
    desc = models.CharField(max_length=256, verbose_name='备注')
