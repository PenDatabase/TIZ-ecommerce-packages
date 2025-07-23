from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models.functions import Coalesce
from .models import Order, OrderItem, Package, Cart, CartItem
from .payment_views import create_paystack_payment


# Remove testview later
def testview(request):
    return render(request, 'test.html', {'collections': None})


class HomeView(TemplateView):
    template_name = "store/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['packages'] = Package.objects.annotate(orders_count=models.Count("order_items__order")).order_by("-orders_count")[:3]
        return context

    
class PackageDetailView(DetailView):
    template_name = "store/packages_detail.html"

    def get_queryset(self):
        return Package.objects.prefetch_related("package_items")
    


class PackageListView(ListView):
    template_name = "store/packages_list.html"
    context_object_name = "packages"

    def get_queryset(self):
        queryset = Package.objects
        search_key = self.request.GET.get("search")

        if search_key:
            queryset = queryset.filter(
                            models.Q(name__icontains=search_key) |
                            models.Q(use_case__icontains=search_key)
                            )

        return queryset.all() 



class CartTemplateView(LoginRequiredMixin, TemplateView):
    template_name="store/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"], created = Cart.objects.prefetch_related("cart_items__package").annotate(
                subtotal=Coalesce(models.Sum("cart_items__total_price"), models.Value(0))
            ).annotate(
                total_price=models.F("subtotal") + 1000
            ).get_or_create(user=self.request.user)
        return context
    



class UpdateCartItemQuantityView(LoginRequiredMixin, UpdateView):
    model = CartItem
    fields = ["quantity"]

    def post(self, request, *args, **kwargs):
        cart_item = self.get_object()
        change = int(request.POST.get("change"))

        if change == 1:
            cart_item.quantity += 1
        if change == -1 and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
        cart= Cart.objects.annotate(
                subtotal=Coalesce(models.Sum("cart_items__total_price"), models.Value(0))
            ).annotate(
                total_price=models.F("subtotal") + 1000
            ).values("subtotal", "total_price").get(user=self.request.user)


        return JsonResponse({
            "success": True,
            "new_quantity": cart_item.quantity,
            "new_price": cart_item.quantity * cart_item.package.price,
            "new_subtotal": cart["subtotal"],
            "new_total_price": cart["total_price"]
        })



def add_to_cart(request, package_pk):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({
                "success": False,
                "detail": "User is not authenticated",
                "redirect": f"{reverse('user:login')}?next={reverse('store:package-listing')}"
            })

        if package_pk:
            cart, cart_created = Cart.objects.get_or_create(user = request.user)
            cart_item, cartitem_created = CartItem.objects.get_or_create(cart=cart, package_id=package_pk)
            cart_item.save()
            
            if not cartitem_created:
                cart_item.quantity += 1
                cart_item.save()

        return JsonResponse({
            "success": True
            })
        

def remove_from_cart(request, cartitem_pk):
    if request.method == "POST":
        cart_item = CartItem.objects.get(pk=cartitem_pk)
        
        if cart_item:
            cart_item.delete()

            return JsonResponse({
                "success": True
            })
        return JsonResponse({
                "success": False,
                "detail": "Cartitem not found"
            })


@login_required
def checkout_cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.cart_items.exists():
       messages.error(request, "Your cart is empty")
       return redirect('store:cart')
    
    order = Order.objects.create(
        user=request.user,
    )

    order_items = [
        OrderItem(
            order=order,
            package=cart_item.package,
            total_price=cart_item.total_price,
            quantity=cart_item.quantity
        )
        for cart_item in cart.cart_items.all()
    ]

    OrderItem.objects.bulk_create(order_items)

    retrieved_order = Order.objects.filter(pk=order.pk).annotate(
                subtotal=Coalesce(models.Sum("order_items__total_price"), models.Value(0))
            ).annotate(
                total_price=models.F("subtotal") + 1000
            ).values("total_price").get()
    
    payment_url = create_paystack_payment(retrieved_order["total_price"], request.user.email, order.id)
    return redirect(payment_url)



class OrderListView(ListView):
    template_name = "store/order-listing.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.prefetch_related("order_items__package").filter(user=self.request.user).all()
    