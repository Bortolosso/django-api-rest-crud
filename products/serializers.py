from rest_framework import serializers
from .models import Product, RequestProduct

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class RequestProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestProduct
        fields = '__all__'
