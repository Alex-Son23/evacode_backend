# Generated by Django 5.0.4 on 2024-06-24 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_contacts_tiktok_alter_review_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionWithVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_file', models.FileField(upload_to='videos/', verbose_name='Видео')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Секция с видео',
                'verbose_name_plural': 'Секции с видео',
            },
        ),
    ]