from django.db import models
import datetime

class medstore(models.Model):
    '''药店模型类'''
    username = models.CharField(max_length=32, verbose_name='药店用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    ypjyxkzcode = models.CharField(max_length=20, verbose_name='药品经营许可证号码')
    gspcode = models.CharField(max_length=13, verbose_name='gsp证书编号')
    name = models.CharField(max_length=20, verbose_name='药店名称')
    desc = models.CharField(max_length=256, verbose_name='药店简介')
    address = models.CharField(max_length=40, verbose_name='药店地址')
    postcode = models.CharField(max_length=20, verbose_name='邮政编码')
    email = models.EmailField(max_length=50, verbose_name="邮箱",default="none")
    emailstatus = models.CharField(max_length=10, verbose_name="邮箱状态",default="未激活",
                                    choices = (("未激活", "未激活"), ("已激活", "已激活")))
    time = models.DateField(auto_now_add=True,null=True, blank=True) #开办时间


# 邮箱验证
class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,
                                 choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.datetime.now())

    class Meta:
        verbose_name = u"2. 邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


