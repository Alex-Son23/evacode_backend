from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from .views import GoodsListAPIView, GoodDetailAPIView, update_data, get_all_goods, GroupListAPIView

urlpatterns = [
    path('goods/', GoodsListAPIView.as_view(), name='goods-list'),
    path('goods/<int:id>/', GoodDetailAPIView.as_view(), name='product-detail'),
    path('categories/', GroupListAPIView.as_view()),
    path('update_data/', update_data),
    path('get_all_goods/', get_all_goods)
]