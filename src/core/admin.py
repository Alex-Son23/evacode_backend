from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Contacts, AboutUs, Banner, Delivery, Slide


class PostAdmin(admin.ModelAdmin):
    pass


class DeliveryAdmin(admin.ModelAdmin):
    pass


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="200">')

    get_image.short_description = "Изображение"


class AboutUsAdmin(admin.ModelAdmin):
    # list_display = ('title', 'description')
    # readonly_fields = ('get_image',)
    #
    # def get_image(self, obj):
    #     return mark_safe(f'<img src={obj.image.url} width="200">')
    #
    # get_image.short_description = "Изображение"
    pass


class ContactsAdmin(admin.ModelAdmin):
    pass


class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="200">')

    get_image.short_description = "Изображение"


admin.site.register(Delivery, DeliveryAdmin)
# admin.site.register(Post, PostAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Slide, SlideAdmin)
