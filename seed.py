import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model
from store.models import Product, Package, PackageItem, Cart, CartItem, Order, OrderItem, Payment

# Initialize Faker
fake = Faker()
User = get_user_model()

def create_users(n=5):
    users = []
    for _ in range(n):
        user = User.objects.create_user(
            email=fake.email(),
            first_name=fake.name(),
            last_name=fake.name(),
            password="password123"
        )
        users.append(user)
    return users

def create_products(n=10):
    products = []
    for _ in range(n):
        product = Product.objects.create(
            name=fake.word().capitalize()
        )
        products.append(product)
    return products

def create_packages(n=5):
    packages = []
    for _ in range(n):
        package = Package.objects.create(
            name=fake.word().capitalize(),
            price=random.randint(500, 5000),
            use_case=fake.sentence(),
            description=fake.paragraph()
        )
        packages.append(package)
    return packages

def create_package_items(packages, products):
    for package in packages:
        selected_products = random.sample(products, k=min(3, len(products)))
        for product in selected_products:
            PackageItem.objects.create(
                package=package,
                product=product,
                quantity=random.randint(1, 10)
            )

def create_carts(users):
    carts = []
    for user in users:
        cart = Cart.objects.create(user=user)
        carts.append(cart)
    return carts

def create_cart_items(carts, packages):
    for cart in carts:
        package = random.choice(packages)
        CartItem.objects.create(
            cart=cart,
            package=package,
            quantity=random.randint(1, 3),
            total_price=package.price * random.randint(1, 3)
        )

def create_orders(users):
    orders = []
    for user in users:
        order = Order.objects.create(user=user)
        orders.append(order)
    return orders

def create_order_items(orders, packages):
    for order in orders:
        package = random.choice(packages)
        OrderItem.objects.create(
            order=order,
            package=package,
            quantity=random.randint(1, 3),
            total_price=package.price * random.randint(1, 3)
        )

def create_payments(users, orders):
    for order in orders:
        Payment.objects.create(
            user=order.user,
            order=order,
            reference=fake.uuid4(),
            status=random.choice([Payment.PENDING, Payment.COMPLETED]),
            completed_at=fake.date_time_this_year(tzinfo=timezone.get_current_timezone()) if random.choice([True, False]) else None
        )

def run():
    print("Seeding database...")
    users = create_users()
    products = create_products()
    packages = create_packages()
    create_package_items(packages, products)
    carts = create_carts(users)
    create_cart_items(carts, packages)
    orders = create_orders(users)
    create_order_items(orders, packages)
    create_payments(users, orders)
    print("Seeding complete!")

if __name__ == "__main__":
    run()
