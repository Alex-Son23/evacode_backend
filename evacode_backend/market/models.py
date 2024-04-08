from django.db import models


class GroupOfGoods(models.Model):
    default_order = models.CharField(max_length=128)
    deleted = models.BooleanField()
    description = models.TextField(blank=True, null=True)
    name = models.CharField(verbose_name="Наименование группы", max_length=128)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    updated = models.DateTimeField()


class GoodsModel(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(GroupOfGoods, on_delete=models.CASCADE, related_name='group')
    type = models.CharField(max_length=128)

    official_price = models.PositiveIntegerField(blank=True, null=True)
    retail_price = models.PositiveIntegerField(blank=True, null=True)
    wholesale_price = models.PositiveIntegerField(blank=True, null=True)
    large_wholesale_price = models.PositiveIntegerField(blank=True, null=True)


class ImageModel(models.Model):
    group = models.ForeignKey(GroupOfGoods, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    good = models.ForeignKey(GoodsModel, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    name = models.CharField(verbose_name="Название", max_length=128)
    sort = models.IntegerField(null=True, blank=True)
    url = models.TextField()
