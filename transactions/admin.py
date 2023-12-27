"""
from django.contrib import admin

from .models import *
# Register your models here.
from django.utils.html import format_html

from django.db import models
import uuid
from bankingsystem.admin_actions import export_as_csv







class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'status', 'date']
    list_filter = ['status', 'date']

    def save_model(self, request, obj, form, change):
        if change:
            original_obj = Payment.objects.get(pk=obj.pk)
            if original_obj.status != 'COMPLETE' and obj.status == 'COMPLETE':
                obj.update_balance()
            elif original_obj.status == 'COMPLETE' and obj.status != 'COMPLETE':
                obj.user.balance -= original_obj.amount
                obj.user.save()
        elif obj.status == 'COMPLETE':
            obj.update_balance()

        super().save_model(request, obj, form, change)


class CryptoWITHDRAWAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_method', 'amount', 'status', 'date')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'user__email')

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data and form.cleaned_data['status'] == 'COMPLETE':
            obj.update_balance()
        obj.save()

admin.site.register(CryptoWITHDRAW, CryptoWITHDRAWAdmin)

admin.site.register(Payment, PaymentAdmin)
admin.site.add_action(export_as_csv, name='export_selected')

"""