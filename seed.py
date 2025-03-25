import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product, Package, PackageItem, Order
from django.contrib.auth.models import User

fake = Faker()

def create_products(n=10):
    products = []
    for _ in range(n):
        product = Product.objects.create(name=fake.word().capitalize())
        products.append(product)
    return products

def create_packages(n=5):
    packages = []
    for _ in range(n):
        package = Package.objects.create(
            name=fake.catch_phrase(),
            inventory=random.randint(12, 13),
            use_case=fake.sentence(),
            price=fake.random_number(),
            description=fake.text()
        )
        packages.append(package)
    return packages

import random

def create_package_items(packages, products):
    for package in packages:
        available_products = products[:]

        if not available_products:
            break
        
        product = random.choice(available_products)
        available_products.remove(product)  # Ensure the product is not selected again

        # Ensure the product is not already in the package
        if not PackageItem.objects.filter(package=package, product=product).exists():
            for _ in range(random.randint(2, 5)):
                PackageItem.objects.create(
                    package=package,
                    product=product,
                    quantity=random.randint(1, 10)
                )


def create_orders(n=10):
    users = list(User.objects.all())
    packages = list(Package.objects.all())
    for _ in range(n):
        user = random.choice(users) if users else None
        package = random.choice(packages)
        Order.objects.create(
            user=user,
            email=fake.email(),
            package=package,
            completed=random.choice([True, False])
        )

def run():
    print("Seeding database...")
    products = create_products()
    packages = create_packages()
    create_package_items(packages, products)
    create_orders()
    print("Database seeding completed!")

if __name__ == "__main__":
    run()
