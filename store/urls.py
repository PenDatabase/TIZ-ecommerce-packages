from django.urls import path
from . import payment_views, views

app_name = "store"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("test/", views.testview, name="testview"), # remove later
    path("packages/", views.PackageListView.as_view(), name="package-listing"),
    path("packages/<int:pk>", views.PackageDetailView.as_view(), name="package-detail"),
    path("cart/", views.CartTemplateView.as_view(), name="cart"),
    path("cart/add/<int:package_pk>", views.add_to_cart, name="add-to-cart"),
    path("cart/checkout/", views.checkout_cart, name="cart-checkout"),
    path("cart/remove/<int:cartitem_pk>", views.remove_from_cart, name="remove-from-cart"),
    path("cartitem/update/<int:pk>", views.UpdateCartItemQuantityView.as_view(), name="update-cartitem-quantity"),
    path("order_history", views.OrderHistoryView.as_view(), name="order-history"),
    path("payment/verify/<int:order_id>", payment_views.verify_paystack_payment_view, name="verify-paystack-payment"),
]
