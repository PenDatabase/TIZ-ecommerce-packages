from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


app_name = "user"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]