# Generated by Django 5.0.4 on 2024-06-20 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_aboutus_options_alter_banner_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='delivery_type',
            field=models.CharField(max_length=128, verbose_name='Тип доставки'),
        ),
    ]