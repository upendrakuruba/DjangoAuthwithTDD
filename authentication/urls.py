from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path("register/",RegistrationView.as_view(), name="register"),
    path("login/",LoginView.as_view(), name="login"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("edit_profile/",Edit_profile, name="edit_profile"),
    path("create_profile/",create_profile, name="create_profile"),
    path("delete/",DeleteView, name="delete"),
    path("dashboard/",Dashboard, name="dashboard"),
    path("changepassword/",ChangePassword, name="changepassword"),
    path("forgotpassword/",RequestResetEmail.as_view(), name="forgotpassword"),
    path("",login_required(HomeView.as_view()), name="home"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("resetpassword_validate/<uidb64>/<token>/", resetpassword_validate, name="resetpassword_validate"),
    path("resetpassword/",resetpassword, name="resetpassword"),
]


