from django.contrib import admin
from django.db.models import Sum
from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ['code'] # remove code when creating order so as to automatically generate
    list_display = ['code', 'user__email', 'date']
    list_per_page = 10
    search_fields = ['user__email', 'code']


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['package', 'order', 'quantity', 'total_price']


@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'use_case']
    list_per_page = 15
    search_fields = ['name', 'use_case']



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'ordered_quantity']
    search_fields = ['name']

    @admin.display(ordering='ordered_quantity')
    def ordered_quantity(self, product: models.Product):
        return product.ordered_quantity or 0
    
    def get_queryset(self, request):
        return models.Product.objects.annotate(
            ordered_quantity = Sum('package_items__package__order_items__quantity')
        )


@admin.register(models.PackageItem)
class PackageItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'package', 'quantity']


@admin.register(models.Cart)
class Cart(admin.ModelAdmin):
    list_display = ['user', 'created_at']


admin.site.register(models.CartItem)
