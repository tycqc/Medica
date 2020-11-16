from django.db import models

class Staff(models.Model):

    username = models.CharField(max_length=32, verbose_name='员工用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    store = models.ForeignKey('store.medstore', verbose_name='药店', on_delete=models.CASCADE)
    name = models.CharField(max_length=32,verbose_name='员工姓名')
    phonenumber = models.ImageField(max_length=11, verbose_name='联系方式')
    desc = models.CharField(max_length=256, verbose_name='员工简介')
