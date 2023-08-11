from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "slug", "parent", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    inlines = [
        ProductSpecificationInline,
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "product_type", "is_active")
    list_filter = ("category", "product_type", "is_active",)
    search_fields = ("title",)
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
