from django.contrib import admin
from django.db.models import Sum, Count, F, Case, When, Value, IntegerField
from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['code', 'user__email', 'created_at']
    list_per_page = 10
    search_fields = ['user__email', 'code']
    readonly_fields = ['code'] # Make code Read Only field so as to prevent from being edited


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
        return product.ordered_quantity
    
    def get_queryset(self, request):
        return models.Product.objects.annotate(
            ordered_quantity = Sum(
                Case(
                        When(package_items__quantity=0, then=Value(1)),
                        default=F('package_items__quantity'),
                        output_field=IntegerField()
                    ) *
                Case(
                    When(package_items__package__order_items__quantity=0, then=Value(1)),
                    default=F('package_items__package__order_items__quantity'),
                    output_field=IntegerField()
                ),
            )
        )


@admin.register(models.PackageItem)
class PackageItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'package', 'quantity']


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'number_of_items']

    def number_of_items(self, cart):
        return cart.number_of_items

    def get_queryset(self, request):
        return models.Cart.objects.annotate(
            number_of_items=Count("cart_items")
        )


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'package', 'quantity', 'total_price']
