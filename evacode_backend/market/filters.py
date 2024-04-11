from django_filters import FilterSet, CharFilter
from .models import GoodsModel


class GoodsFilter(FilterSet):
    id = CharFilter(lookup_expr='exact', required=False)
    category__id = CharFilter(field_name='category__id', lookup_expr='exact', required=False)

    class Meta:
        model = GoodsModel
        fields = ['id', 'category__id']
