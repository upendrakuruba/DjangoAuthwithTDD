from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path("register/",RegistrationView.as_view(), name="register"),
    path("login/",LoginView.as_view(), name="login"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("",login_required(HomeView.as_view()), name="home"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
