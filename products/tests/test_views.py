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
        self.assertEqual(response.data, {
            "message": "Não existe registro com o ID: 30.",
            "status": 404
        })


class CreateNewProductTest(TestCase):
    """ Teste criação de produto """

    def setUp(self):
        self.valid_payload = {
            'name': 'Meia do Internacional',
            'unity_value': 40,
            'quantity_product': 18,
        }
        self.invalid_payload = {
            'name': '',
            'unity_value': 40,
            'quantity_product': 18,
        }
        
        self.valid_payload_equall = {
            'name': 'Meia do Sao Paulo',
            'unity_value': 40,
            'quantity_product': 18,
        }
        
        self.juventus = Product.objects.create(
            name='Meia do Sao Paulo', unity_value=480, quantity_product=6, status="Disponível"
        )

    def test_create_valid_product(self):
        response = client.post(
            reverse('get_post_product'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, {
            "message": "Produto adicioando com sucesso.",
            "data": {
                "id": 5,
                "name": "Meia do Internacional",
                "quantity_product": 18,
                "status": "Disponivel",
                "unity_value": 40
            },
            "status": 201
        })
        
    
    def test_equall_name_invalid_product(self):
        response = client.post(
            reverse('get_post_product'),
            data=json.dumps(self.valid_payload_equall),
            content_type='application/json'
        )
        self.assertEqual(response.data, {
            "message": "Produto: Meia do Sao Paulo, já cadastrado no sistema.",
            "status": 400
        })

    def test_create_invalid_product(self):
        response = client.post(
            reverse('get_post_product'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, {
            "message": "verifique seu object payload.",
            "data": {
                "name": [
                    "This field may not be blank."
                ]
            },
            "status": 400
        })

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
            'name': 'Camiseta do Corinthians',
            'unity_value': 450,
            'quantity_product': 4,
        }
        self.invalid_payload_equall_name = {
            'name': 'Camiseta do Barcelona',
            'unity_value': 450,
            'quantity_product': 4,
        }
        self.invalid_payload = {
            'name': '',
            'unity_value': 40,
            'quantity_product': 18,
        }

    def test_valid_update_product(self):
        response = client.put(
            reverse('get_delete_update_product', kwargs={'pk': self.sao_paulo.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, {
            "message": "Produto atualizado com sucesso. ID: 28",
            "data": {
                "id": 28,
                "name": "Camiseta do Corinthians",
                "unity_value": 450,
                "quantity_product": 4,
                "status": "Disponivel"
            },
            "status": 204
        })
        
    def test_invalid_update_product_equall_name(self):
        response = client.put(
            reverse('get_delete_update_product', kwargs={'pk': self.sao_paulo.pk}),
            data=json.dumps(self.invalid_payload_equall_name),
            content_type='application/json'
        )
        self.assertEqual(response.data, {
            "message": "Já existe um produto com o nome: Camiseta do Barcelona",
            "data": {
                "name": "Camiseta do Barcelona",
                "unity_value": 450,
                "quantity_product": 4
            },
            "status": 400
        })

    def test_invalid_update_product(self):
        response = client.put(
            reverse('get_delete_update_product', kwargs={'pk': self.sao_paulo.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        print("reponse", response.data)
        self.assertEqual(response.data, {
            "name": [
                "This field may not be blank."
            ]
        })


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
        self.assertEqual(response.data, {
            "message": "Produto: Camiseta do São Paulo, deletado com sucesso no sistema.",
            "status": 204
        })

    def test_invalid_delete_product(self):
        response = client.delete(
            reverse('get_delete_update_product', kwargs={'pk': 30}))
        self.assertEqual(response.data, {
            "message": "Não existe registro com o ID: 30.",
            "status": 404
        })