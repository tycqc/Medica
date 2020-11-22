from django.db import models

class User(models.Model):
    phone = models.CharField(max_length=11, verbose_name='联系方式')
    token = models.CharField(verbose_name='用户TOKEN', max_length=64, null=True, blank=True)
    username = models.CharField(max_length=32, verbose_name='顾客姓名',null=True, blank=True)
    name = models.CharField(max_length=32,verbose_name='微信昵称',null=True, blank=True)
    desc = models.CharField(max_length=256, verbose_name='备注',null=True, blank=True)
