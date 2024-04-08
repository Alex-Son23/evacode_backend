from django.shortcuts import render

from .pagination import CustomPagination
from .utils import BusinessRuService, BusinessRuAPIClient
from rest_framework import generics
from .models import GoodsModel
from .serializers import GoodsSerializer


class GoodsListAPIView(generics.ListAPIView):
    queryset = GoodsModel.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = CustomPagination


class GoodDetailAPIView(generics.RetrieveAPIView):
    queryset = GoodsModel.objects.all()
    serializer_class = GoodsSerializer
    lookup_field = 'id'
