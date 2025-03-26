from django.urls import path
from . import views


app_name = "store"


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("packages/", views.PackageListView.as_view(), name="package-listing"),
    path("packages/<int:pk>", views.PackageDetailView.as_view(), name="package-detail"),
    path("cart/", views.CartTemplateView.as_view(), name="cart"),
    path("cart/add/<int:package_pk>", views.add_to_cart, name="add-to-cart"),
    path("cart/remove/<int:cartitem_pk>", views.remove_from_cart, name="remove-from-cart"),
    path("cartitem/update/<int:pk>", views.UpdateCartItemQuantityView.as_view(), name="update-cartitem-quantity")
]
