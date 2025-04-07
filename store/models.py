import uuid
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError


User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Package(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    use_case = models.CharField(max_length=255)
    description = models.TextField()
    

    def __str__(self):
        return self.name


class PackageItem(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="package_items")
    product = models.ForeignKey(Product, models.PROTECT, related_name="package_items")
    quantity = models.PositiveIntegerField()
    
    # A Package cannot contain one product more than one e.g canno have 5 shirts and 6 shirts, instead will have 11 shirts
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['package', 'product'], name="package_product Uniqueness")
        ]



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, related_name="cart_items")
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name="cart_items")
    total_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.total_price = self.package.price * self.quantity
        return super().save()
    
    # A cart cannot contain more than one instance of a package
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'package'], name="cart_package_uniqueness")
        ]



def generate_order_code():
    return f"ORD-{datetime.now().strftime('%S%d%m%y')}-{uuid.uuid4().hex[:6].upper()}"

class Order(models.Model):
    NOT_YET_DELIVERED = "NOT YET DELIVERED"
    DELIVERED = "DELIVERED"
    STATUS_CHOICES = {
        NOT_YET_DELIVERED: NOT_YET_DELIVERED,
        DELIVERED: DELIVERED
    }
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    code = models.CharField(max_length=19, unique=True, blank=True, default=generate_order_code)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=17, choices=STATUS_CHOICES, default=NOT_YET_DELIVERED)

    def __str__(self):
        return self.code


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name="order_items")
    total_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.total_price = self.package.price * self.quantity
        return super().save()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'package'], name="order_package_uniqueness")
        ]


class Payment(models.Model):
    PENDING = "PENDING"
    COMPLETED = "COMPLETE"
    PAYMENT_STATUS = {
        PENDING :"PENDING",
        COMPLETED :"COMPLETED"
    }
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="payments", null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name="payments", null=True)
    amount = models.PositiveIntegerField()
    reference = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=9, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)