from django.contrib import admin
from django.utils.html import format_html
from .models import Car, Order

class CarAdmin(admin.ModelAdmin):
    list_display = ['CarID', 'carName', 'carType', 'carDescription', 'carRate', 'display_car_pic', 'status']

    def display_car_pic(self, obj):
        if obj.carPic:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.carPic.url)
        else:
            return "No Image"

    display_car_pic.short_description = 'Car Picture'

admin.site.register(Car, CarAdmin)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('orderNumber', 'userid', 'carid', 'carName', 'startDate', 'endDate', 'total', 'duration', 'status')
    search_fields = ('orderNumber', 'carName')
    list_filter = ('startDate', 'status')  # Add 'status' to the list_filter
    ordering = ('-startDate',)  # Optional: Order by start date descending

admin.site.register(Order, OrdersAdmin)
