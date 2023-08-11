from django.contrib import admin

from .models import DeliveryOptions


@admin.register(DeliveryOptions)
class DeliveryOptionsAdmin(admin.ModelAdmin):
    list_display = ("delivery_name", "delivery_price", "delivery_method", "is_active")
    list_filter = ("delivery_method", "is_active",)
    search_fields = ("delivery_name", )
