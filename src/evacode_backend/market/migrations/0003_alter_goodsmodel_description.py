# Generated by Django 5.0.3 on 2024-04-08 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_alter_goodsmodel_large_wholesale_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsmodel',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]