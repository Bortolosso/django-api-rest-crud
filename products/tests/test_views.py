import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Product
from ..serializers import ProductSerializer


client = Client()


class GetAllProductsTest(TestCase):
    """ Modulos de teste para GET todos os produtos API """

    def setUp(self):
        Product.objects.create(
            name='Camiseta do Barcelona', unity_value=500, quantity_product=10, status="Disponível"
        )
        Product.objects.create(
            name='Camiseta do São Paulo', unity_value=350, quantity_product=15, status="Disponível"
        )
        Product.objects.create(
            name='Camiseta do Inter', unity_value=400, quantity_product=8, status="Disponível"
        )
        Product.objects.create(
            name='Camiseta do Juventus', unity_value=480, quantity_product=6, status="Disponível"
        )

    def test_get_all_products(self):
        response = client.get(reverse('get_post_product'))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleProductTest(TestCase):
    """ Modulos de teste para GET unico """

    def setUp(self):
        self.barcelona = Product.objects.create(
            name='Camiseta do Barcelona', unity_value=500, quantity_product=10, status="Disponível"
        )
        self.sao_paulo = Product.objects.create(
            name='Camiseta do São Paulo', unity_value=350, quantity_product=15, status="Disponível"
        )
        self.inter = Product.objects.create(
            name='Camiseta do Inter', unity_value=400, quantity_product=8, status="Disponível"
        )
        self.juventus = Product.objects.create(
            name='Camiseta do Juventus', unity_value=480, quantity_product=6, status="Disponível"
        )

    def test_get_valid_single_product(self):
        response = client.get(
            reverse('get_delete_update_product', kwargs={'pk': self.inter.pk}))
        product = Product.objects.get(pk=self.inter.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        response = client.get(
            reverse('get_delete_update_product', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewProductTest(TestCase):
    """ Teste criação de produto """

    def setUp(self):
        self.valid_payload = {
            'name': 'Meia do Internacional',
            'unity_value': 40,
            'quantity_product': 18,
            'status': 'Enviado'
        }
        self.invalid_payload = {
            'name': '',
            'unity_value': 40,
            'quantity_product': 18,
            'status': ''
        }

    def test_create_valid_product(self):
        response = client.post(
            reverse('get_post_product'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        response = client.post(
            reverse('get_post_product'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleProductTest(TestCase):
    """ Teste de atualização de dados já existentes """

    def setUp(self):
        self.barcelona = Product.objects.create(
            name='Camiseta do Barcelona', unity_value=500, quantity_product=10, status="Disponível"
        )
        self.sao_paulo = Product.objects.create(
            name='Camiseta do São Paulo', unity_value=350, quantity_product=15, status="Disponível"
        )
        
        self.valid_payload = {
            'name': 'Camiseta do Barcelona',
            'unity_value': 450,
            'quantity_product': 4,
            'status': 'Enviado'
        }
        self.invalid_payload = {
            'name': '',
            'unity_value': 40,
            'quantity_product': 18,
            'status': ''
        }

    def test_valid_update_product(self):
        response = client.put(
            reverse('get_delete_update_product', kwargs={'pk': self.sao_paulo.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_product(self):
        response = client.put(
            reverse('get_delete_update_product', kwargs={'pk': self.sao_paulo.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleProductTest(TestCase):
    """ Teste de deleção de dado """

    def setUp(self):
        self.barcelona = Product.objects.create(
            name='Camiseta do Barcelona', unity_value=500, quantity_product=10, status="Disponível"
        )
        self.sao_paulo = Product.objects.create(
            name='Camiseta do São Paulo', unity_value=350, quantity_product=15, status="Disponível"
        )

    def test_valid_delete_product(self):
        response = client.delete(
            reverse('get_delete_update_product', kwargs={'pk': self.sao_paulo.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_product(self):
        response = client.delete(
            reverse('get_delete_update_product', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)