from django.db import models

class Orders(models.Model):
    #model的choices
    PAY_METHOD_CHOICES = (
        (0, '现金支付'),
        (1, '微信支付'),
        (2, '支付宝')
    )

    ORDER_STATUS_CHOICES = (
        (0, '待支付'),
        (1, '待配送'),
        (2, '已送达'),
        (3, '待评价'),
        (4, '已完成')
    )
    order_id = models.CharField(max_length=32, verbose_name='订单ID', primary_key=True)
    staff = models.ForeignKey('staff.Staff', verbose_name='操作员', on_delete=models.CASCADE, null=True, blank=True)
    drugstore = models.ForeignKey('store.Medstore', verbose_name='药店', on_delete=models.CASCADE)
    addr = models.CharField(null=True, blank=True, max_length=128, verbose_name='收货地址')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=0, verbose_name='支付方式')
    total_count = models.IntegerField(default=1, verbose_name='数量')
    med_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='药品总价')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='配送费')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    time = models.DateTimeField(auto_now_add=True)

class OrderGoods(models.Model):
    '''订单药品模型类'''
    order = models.ForeignKey('Orders', verbose_name='订单', on_delete=models.CASCADE)
    sku = models.ForeignKey('medicine.Medicine', verbose_name='药品', on_delete=models.CASCADE)
    count = models.IntegerField(default=1, verbose_name='数目')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    comment = models.CharField(null=True, blank=True, max_length=256, default='', verbose_name='评论')

