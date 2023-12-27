from django.contrib import admin

# Register your models here.
from .models import Courier

class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'tracking_id', 'service', 'date_sent', 'date_arrival')
    list_filter = ('service', 'date_sent', 'date_arrival')
    search_fields = ('name', 'tracking_id', 'service', 'date_sent', 'date_arrival')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'service', 'tracking_id')
        }),
        ('Sender and Receiver', {
            'fields': ('sender', 'reciever', 'contact_info')
        }),
        ('Location and Dates', {
            'fields': ('address', 'current_location', 'map_location', 'date_sent', 'date_arrival')
        }),
        ('Details', {
            'fields': ('quantity', 'price')
        }),
        ('Photo for the PACKAGE', {
            'fields': ('avatar',)
        }),
        ('Photo ID', {
            'fields': ('photo_id',)
        }),
    )

    

admin.site.register(Courier, CourierAdmin)