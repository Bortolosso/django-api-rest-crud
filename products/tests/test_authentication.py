from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from rest_framework import status
from django.urls import reverse

from ..models import Product
from ..serializers import ProductSerializer


client = APIClient()


class TestAuthAPIViews(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')
        Product.objects.create(
            name='Camiseta do Barcelona', unity_value=500, quantity_product=10, status="Disponível"
        )

    def test_ListAccounts_not_authenticated(self):
        client.force_authenticate(None)
        response = client.get(reverse('get_post_product'))
        self.assertEqual(response.status_code, 401)

    def test_ListAccounts_authenticated(self):
        client.force_authenticate(user=self.admin)
        response = client.get(reverse('get_post_product'))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
