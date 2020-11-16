from django.db import models

class Medicine(models.Model):
    '''药品SKU模型类'''
    status_choices = (
        (0, '暂无'),
        (1, '暂停销售'),
    )

    drugstore = models.ForeignKey('store.Medstore', verbose_name='药店', on_delete=models.CASCADE)
    medicinecode = models.CharField(max_length=14, verbose_name='国家药品编码')
    name = models.CharField(max_length=20, verbose_name='药品名称')
    type = models.CharField(max_length=20, verbose_name='药品种类')
    desc = models.CharField(max_length=256, verbose_name='药品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='药品价格')
    unite = models.CharField(max_length=20, verbose_name='药品生产单位')
    image = models.ImageField(upload_to='medicine_image', verbose_name='药品图片')
    stock = models.IntegerField(default=1, verbose_name='药品库存')
    sales = models.IntegerField(default=0, verbose_name='药品销量')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='药品状态')

    class Meta:
        db_table = 'medicine_SKU'
        verbose_name = '药品SKU'
        verbose_name_plural = verbose_name

class Cart(models.Model):
    C_store = models.ForeignKey('store.medstore', on_delete=models.CASCADE)
    C_goods = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    C_goods_num = models.IntegerField(default=1)

# class GoodsImage(models.Model):
#     #药品图片模型类
#     sku = models.ForeignKey('medicineSKU', verbose_name='药品', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='medicine', verbose_name='图片路径')
#
#     class Meta:
#         db_table = 'medicine_image'
#         verbose_name = '药品图片'
#         verbose_name_plural = verbose_name