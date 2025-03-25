import uuid
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.core.exceptions import ValidationError


user = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    # inventory = models.PositiveIntegerField()
    use_case = models.CharField(max_length=255)
    description = models.TextField()
    

    def __str__(self):
        return self.name


class PackageItem(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="package_items")
    product = models.ForeignKey(Product, models.PROTECT, related_name="package_items")
    quantity = models.IntegerField()
    
    def clean(self):
        super().clean()

        if PackageItem.objects.filter(package=self.package, product=self.product).exists():
            raise ValidationError({"product": f"{self.product} has already been added to this package"})
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)



class Cart(models.Model):
    user = models.OneToOneField(user, on_delete=models.PROTECT, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, related_name="cart_items")
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name="cart_items")
    total_price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.total_price = self.package.price * self.quantity
        return super().save()



class Order(models.Model):
    user = models.ForeignKey(user, on_delete=models.PROTECT, related_name="orders")
    email = models.EmailField()
    packages = models.ManyToManyField(Package, related_name="orders")
    code = models.CharField(max_length=19, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # generate order number
        if not self.code:
            self.code = f"ORD-{datetime.now().strftime('%S%d%m%y')}-{uuid.uuid4().hex[:6].upper()}"

        # with transaction.atomic():
        #     if self.package.inventory > 0:
        #         Package.objects.filter(pk=self.package.pk).update(inventory=models.F("inventory") - 1)
        #     else:
        #         raise ValidationError({"package":f"#{self.package.pk} - {self.package.name} is out of stock"})
        
        super().save(*args, **kwargs)


    def __str__(self):
        return self.code
