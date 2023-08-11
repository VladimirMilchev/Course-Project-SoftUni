from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Customer, Address
from ..catalogue.admin import CategoryAdmin, ProductTypeAdmin, ProductAdmin
from ..catalogue.models import ProductType, Product, Category
from ..checkout.admin import DeliveryOptionsAdmin
from ..checkout.models import DeliveryOptions
from ..orders.admin import OrderItemAdmin, OrderAdmin
from ..orders.models import OrderItem, Order


class AddressInline(admin.StackedInline):
    model = Address
    fieldsets = (
        ('Personal Information:', {
            'fields': ('full_name', 'phone',),
            'classes': ('wide',),
        }),
        ('Address Details', {
            'fields': ('address_line', 'address_line2', 'town_city', 'postcode', 'delivery_instructions', 'default'),
            'classes': ('collapse',),
        }),
    )

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            num_addresses = Address.objects.filter(customer=obj).count()
            return max(0, num_addresses - 1)
        return 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "mobile", "is_active")
    list_filter = ("is_active",)
    search_fields = ("email", "name", "mobile",)
    inlines = [
        AddressInline,
    ]


class StaffAdminSite(AdminSite):
    site_header = "Estore Admin"
    site_title = "Estore Staff Admin Portal"
    index_title = "Welcome to Estore Staff Portal"


staff_admin_site = StaffAdminSite(name='estore_admin')
staff_admin_site.register(Category, CategoryAdmin)
staff_admin_site.register(ProductType, ProductTypeAdmin)
staff_admin_site.register(Product, ProductAdmin)
staff_admin_site.register(DeliveryOptions, DeliveryOptionsAdmin)
staff_admin_site.register(OrderItem, OrderItemAdmin)
staff_admin_site.register(Order, OrderAdmin)

