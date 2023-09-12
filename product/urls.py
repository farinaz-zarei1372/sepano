from django.urls import path
from . import views
from .models import Product
from product.views import ProductViewset


urlpatterns = [
    # path("", views.ProductAPIView.as_view()),
    # path("list/", views.ProductlistAPIView.as_view()),
    # path("delete/<str:name>/", views.DeleteProductAPIView.as_view()),
    # path("edit/<str:name>/", views.EditProductAPIView.as_view())
]


