from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from .views import GoodsListAPIView, GoodDetailAPIView

urlpatterns = [
    path('products/', GoodsListAPIView.as_view(), name='goods-list'),
    path('products/<int:id>/', GoodDetailAPIView.as_view(), name='product-detail'),
]