from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
Order, OrderItems, Newsletter,
FAQ, ContactUs, Settings,
Shipping, Payment,Country,
About,
)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):


    def has_delete_permission(self, request, obj=None):
        if request.user.email == 'admin@gmail.com':
            return True
        else:
            return False
    
    def has_add_permission(self, request):
        if request.user.email == 'admin@gmail.com':
            return True
        else:
            return False
        
# admin.site.register(FAQ)


class FaqAdmin(TranslationAdmin):
    list_display =('question', 'answer', 'order' )

admin.site.register(FAQ, FaqAdmin)


class AboutAdmin(TranslationAdmin):
    list_display = ('title',)

admin.site.register(About, AboutAdmin)


admin.site.register(OrderItems)
admin.site.register(Order)
admin.site.register(Newsletter)
admin.site.register(ContactUs)
admin.site.register(Shipping)
admin.site.register(Payment)
admin.site.register(Country)