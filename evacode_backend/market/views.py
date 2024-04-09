from django.shortcuts import render

from .pagination import CustomPagination, AllObjectPagination
from .utils import BusinessRuService, BusinessRuAPIClient
from rest_framework import generics
from .models import GoodsModel, GroupOfGoods
from .serializers import GoodsSerializer, GroupOfGoodsSerializer
from django.http import HttpResponse, JsonResponse


class GoodsListAPIView(generics.ListAPIView):
    queryset = GoodsModel.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = CustomPagination


class GoodDetailAPIView(generics.RetrieveAPIView):
    queryset = GoodsModel.objects.all()
    serializer_class = GoodsSerializer
    lookup_field = 'id'


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
