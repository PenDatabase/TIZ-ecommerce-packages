from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from .models import Package, Cart, CartItem



class HomeView(TemplateView):
    template_name = "store/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['packages'] = Package.objects.annotate(orders_count=models.Count("orders")).order_by("-orders_count")[:3]
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
                            models.Q(use_case__icontains=search_key) |
                            models.Q(description__icontains=search_key)
                            )

        return queryset.all() 



class CartTemplateView(LoginRequiredMixin, TemplateView):
    template_name="store/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"], created = Cart.objects.prefetch_related("cart_items__package").annotate(
            subtotal=models.Sum("cart_items__total_price"),
            total_price=models.F("subtotal") + 1000).get_or_create(user=self.request.user)
        return context
    



class UpdateCartItemQuantityView(LoginRequiredMixin, UpdateView):
    model = CartItem
    fields = ["quantity"]

    def get_object(self, queryset = None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(CartItem, pk=pk)
    

    def post(self, request, *args, **kwargs):
        cart_item = self.get_object()
        change = int(request.POST.get("change"))

        if change == 1:
            cart_item.quantity += 1
        if change == -1 and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
        cart= Cart.objects.filter(user=self.request.user).annotate(
            subtotal=models.Sum("cart_items__total_price"),
            total_price=models.F("subtotal") + 1000).values("subtotal", "total_price").first()


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
            cart, created = Cart.objects.get_or_create(user = request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, package_id=package_pk)

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return JsonResponse({
                "success": True
                })
        
        return JsonResponse({
                "success": False,
                "detail": f"Invalid paramater '{package_pk}'"
            })