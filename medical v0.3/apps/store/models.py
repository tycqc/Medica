from django.db import models


class medstore(models.Model):
    '''药店模型类'''
    username = models.CharField(max_length=32, verbose_name='药店用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    ypjyxkzcode = models.CharField(max_length=20, verbose_name='药品经营许可证号码')
    gspcode = models.CharField(max_length=13 , verbose_name='gsp证书编号')
    name = models.CharField(max_length=20, verbose_name='药店名称')
    desc = models.CharField(max_length=256, verbose_name='药店简介')
    address = models.CharField(max_length=40, verbose_name='药店地址')
    postcode = models.CharField(max_length=20, verbose_name='邮政编码')
    time = models.DateField(auto_now_add=True,null=True, blank=True) #开办时间



