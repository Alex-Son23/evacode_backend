# Generated by Django 5.0.4 on 2024-06-24 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
    ]
