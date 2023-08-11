from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "created", "total_paid", "billing_status")
    list_filter = ("created", "billing_status",)
    search_fields = ("id", "full_name", "email", "phone", )
    ordering = ("-billing_status",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity")
    list_filter = ("order__created",)
    search_fields = ("order__id", "product__title", "product__description")
