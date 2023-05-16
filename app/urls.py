from django.urls import path

from . import views

urlpatterns = [
    path("user/signup/", views.SignupAPIView.as_view(), name="user-signup"),
    path("user/login/", views.LoginAPIView.as_view(), name="user-login"),
    path("accounts/", views.AccountsAPIView.as_view(), name="user-accounts"),
]
