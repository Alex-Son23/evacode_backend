from django.contrib import admin
from .models import Post, Contacts, AboutUs, Banner, Delivery, Slide


class PostAdmin(admin.ModelAdmin):
    pass


class DeliveryAdmin(admin.ModelAdmin):
    pass


class BannerAdmin(admin.ModelAdmin):
    pass


class AboutUsAdmin(admin.ModelAdmin):
    pass


class ContactsAdmin(admin.ModelAdmin):
    pass


class SlideAdmin(admin.ModelAdmin):
    pass


admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Slide, SlideAdmin)

