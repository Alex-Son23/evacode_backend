from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class Post(models.Model):
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text


class Banner(models.Model):
    name = models.CharField(verbose_name="Поле для поиска", max_length=128)
    title = models.CharField(verbose_name="Название", max_length=128)
    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class AboutUs(models.Model):
    name = models.CharField(verbose_name="Поле для поиска", max_length=128)
    image = models.ImageField(verbose_name="Картинка", upload_to="images/")
    title = models.CharField(verbose_name="Название", max_length=128)
    description = RichTextUploadingField()

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'


class Delivery(models.Model):
    delivery_type = models.CharField(verbose_name="Тип доставки")
    delivery_description = RichTextUploadingField()

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'


class Slide(models.Model):
    image = models.ImageField(verbose_name="Картинка", upload_to="images/")
    title = models.CharField(verbose_name="Название", max_length=128)
    description = RichTextUploadingField()

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'


class Contacts(models.Model):
    telegram = models.CharField(verbose_name="Telegram", max_length=128)
    instagram = models.CharField(verbose_name="Instagram", max_length=128)
    facebook = models.CharField(verbose_name="Facebook", max_length=128)
    address = models.CharField(verbose_name="Address", max_length=128)
    phone = models.CharField(verbose_name="Phone", max_length=128)
    email = models.CharField(verbose_name="Email", max_length=128)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'