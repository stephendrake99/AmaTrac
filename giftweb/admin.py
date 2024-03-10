from django.contrib import admin
from .models import *
from .models import Contactor
from giftsite.admin_actions import export_as_csv

class ContactAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'subject', 'email', 'contact_date')
  list_display_links = ('id', 'name')
  search_fields = ('name', 'email', 'subject')
  list_per_page = 20

admin.site.register(Contactor, ContactAdmin)
admin.site.register(Product)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount', 'status', 'completed')
    list_filter = ('status', 'completed')
    actions = ['mark_as_complete']

    def mark_as_complete(self, request, queryset):
        queryset.update(status='COMPLETED', completed=True)
    mark_as_complete.short_description = "Mark selected payments as complete"

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PremiumProduct)
admin.site.register(Blog)
admin.site.register(Video)
admin.site.add_action(export_as_csv, name='export_selected')