from django.shortcuts import render

from .filters import GoodsFilter
from django_filters import rest_framework as filters
from .pagination import CustomPagination, AllObjectPagination
from .utils import BusinessRuService, BusinessRuAPIClient
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .models import GoodsModel, GroupOfGoods
from .serializers import GoodsSerializer, GroupOfGoodsSerializer
from django.http import HttpResponse, JsonResponse
from django_filters.rest_framework import DjangoFilterBackend


class GoodsAPIView(ModelViewSet):
    queryset = GoodsModel.objects.all().distinct()
    serializer_class = GoodsSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GoodsFilter


class GroupListAPIView(generics.ListAPIView):
    queryset = GroupOfGoods.objects.order_by('id')
    serializer_class = GroupOfGoodsSerializer
    pagination_class = AllObjectPagination


def update_data(request):
    b = BusinessRuService()
    b.group_to_model()
    b.goods_to_model()
    return HttpResponse(content='Data updated!', status=200)


def get_all_goods(request):
    mast_point = GoodsSerializer(GoodsModel.objects.all(), many=True).data
    data = {'result': mast_point}
    # out.write(json.dumps(data, ensure_ascii=False))
    return JsonResponse(data, safe=False)
