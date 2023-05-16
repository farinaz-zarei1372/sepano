from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductAPIView.as_view()),
    path("list/", views.ProductlistAPIView.as_view()),
    # path("accounts/", views.StudentAPIView.as_view(), name="user-accounts"),
]