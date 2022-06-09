import django_filters
from .models import Product, RequestProduct


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['status']


class RequestProductFilter(django_filters.FilterSet):
    class Meta:
        model = RequestProduct
        fields = ['order_status']
