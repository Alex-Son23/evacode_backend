from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import update_data, get_all_goods, GroupListAPIView, GoodsAPIView


router = DefaultRouter()
router.register('goods', GoodsAPIView, basename='good')

urlpatterns = [
    path("", include(router.urls)),
    path('categories/', GroupListAPIView.as_view()),
    path('update_data/', update_data),
    path('get_all_goods/', get_all_goods)
]