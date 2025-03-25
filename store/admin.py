from django.contrib import admin

from . import models

admin.site.register(models.Order)
admin.site.register(models.Package)
admin.site.register(models.Product)
admin.site.register(models.PackageItem)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)

