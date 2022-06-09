import json

from rest_framework import status
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from django.urls import reverse

from ..models import Product, RequestProduct
from ..serializers import ProductSerializer, RequestProductSerializer

client = APIClient()


class GetAllProductsTest(TestCase):
    """ Modulos de teste para GET todos os produtos API """

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')
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
        client.force_authenticate(user=self.admin)
        response = client.get(reverse('get_post_product'))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleProductTest(TestCase):
    """ Modulos de teste para GET unico """

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')
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
        client.force_authenticate(user=self.admin)
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
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')
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
        client.force_authenticate(user=self.admin)
        response = client.post(
            reverse('get_post_product'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        response_data = response.data
        response_data = response_data.get('data')
        id_dynamic_response = response_data.get('id')
        self.assertEqual(response.data, {
            "message": "Produto adicioando com sucesso.",
            "data": {
                "id": id_dynamic_response,
                "name": "Meia do Internacional",
                "quantity_product": 18,
                "status": "Disponivel",
                "unity_value": 40
            },
            "status": 201
        })

    def test_equall_name_invalid_product(self):
        client.force_authenticate(user=self.admin)
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
        client.force_authenticate(user=self.admin)
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
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')
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
        client.force_authenticate(user=self.admin)
        response = client.put(
            reverse('get_delete_update_product',
                    kwargs={'pk': self.sao_paulo.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        response_data = response.data
        response_data = response_data.get('data')
        id_dynamic_response = response_data.get('id')
        self.assertEqual(response.data, {
            "message": "Produto atualizado com sucesso. ID: {0}".format(id_dynamic_response),
            "data": {
                "id": id_dynamic_response,
                "name": "Camiseta do Corinthians",
                "unity_value": 450,
                "quantity_product": 4,
                "status": "Disponivel"
            },
            "status": 204
        })

    def test_invalid_update_product_equall_name(self):
        client.force_authenticate(user=self.admin)
        response = client.put(
            reverse('get_delete_update_product',
                    kwargs={'pk': self.sao_paulo.pk}),
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
        client.force_authenticate(user=self.admin)
        response = client.put(
            reverse('get_delete_update_product',
                    kwargs={'pk': self.sao_paulo.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.data, {
            "name": [
                "This field may not be blank."
            ]
        })


class DeleteSingleProductTest(TestCase):
    """ Teste de deleção de dado """

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')
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
        client.force_authenticate(user=self.admin)
        response = client.delete(
            reverse('get_delete_update_product', kwargs={'pk': 30}))
        self.assertEqual(response.data, {
            "message": "Não existe registro com o ID: 30.",
            "status": 404
        })


class GetAllRequestsProductsTest(TestCase):
    """ Modulos de teste para GET todos os produtos API """

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')
        RequestProduct.objects.create(
            product='Camiseta do Barcelona',
            unity_value_request=500,
            quantity_product_request=10,
            requester="User",
            forwarding_agent="Correios",
            address="Avenida Paulista, 4093 São Paulo-SP",
            order_status="Enviado"
        )
        RequestProduct.objects.create(
            product='Camiseta do Internacional',
            unity_value_request=500,
            quantity_product_request=10,
            requester="User",
            forwarding_agent="Correios",
            address="Avenida Paulista, 4093 São Paulo-SP",
            order_status="Enviado"
        )

    def test_get_all_request_products(self):
        client.force_authenticate(user=self.admin)
        response = client.get(reverse('get_post_request_product'))
        products = RequestProduct.objects.all()
        serializer = RequestProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewRequestProductTest(TestCase):
    """ Teste solicitação de produto """

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')
        self.inter = Product.objects.create(
            name='Camiseta do Inter', unity_value=400, quantity_product=800, status="Disponível"
        )
        self.valid_payload = {
            "product": "Camiseta do Inter",
            "unity_value_request": 500,
            "quantity_product_request": 40,
            "requester": "User",
            "forwarding_agent": "Correios",
            "address": "Avenida Paulista, 4093 São Paulo-SP",
            "order_status": "Enviado"
        }

        self.invalid_payload = {
            "product": "",
            "unity_value_request": 500,
            "quantity_product_request": 40,
            "requester": "User",
            "forwarding_agent": "Correios",
            "address": "Avenida Paulista, 4093 São Paulo-SP",
            "order_status": "Enviado"
        }
        
        self.invalid_payload_name_not_exist = {
            "product": "Meia da Argentina",
            "unity_value_request": 500,
            "quantity_product_request": 40,
            "requester": "User",
            "forwarding_agent": "Correios",
            "address": "Avenida Paulista, 4093 São Paulo-SP",
            "order_status": "Enviado"
        }

    def test_create_valid_product(self):
        client.force_authenticate(user=self.admin)
        response = client.post(
            reverse('get_post_request_product'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        response_data = response.data
        data_product_updated = response_data.get("data_product_updated")
        data_request_product = response_data.get("data_request_product")
        data_product_updated_id = data_product_updated.get("id")
        data_request_product_id = data_request_product.get("id")
        data_request_product_date = data_request_product.get("solicitation")
        self.assertEqual(response.data, {
            "message": "Solicitação do pedido Camiseta do Inter envidada com sucesso.",
            "data_product_updated": {
                "id": data_product_updated_id,
                "name": "Camiseta do Inter",
                "unity_value": 400,
                "quantity_product": 760,
                "status": "Disponivel"
            },
            "data_request_product": {
                "id": data_request_product_id,
                "product": "Camiseta do Inter",
                "unity_value_request": 500,
                "quantity_product_request": 40,
                "solicitation": str(data_request_product_date),
                "requester": "User",
                "forwarding_agent": "Correios",
                "address": "Avenida Paulista, 4093 São Paulo-SP",
                "order_status": "Enviado"
            },
            "status": 201
        })

    def test_name_invalid_product(self):
        client.force_authenticate(user=self.admin)
        response = client.post(
            reverse('get_post_request_product'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.data, {
            "message": "Payload incorreto, parametro product obrigatorio.",
            "status": 400
        })
        
    def test_name_invalid_product_not_exist(self):
        client.force_authenticate(user=self.admin)
        response = client.post(
            reverse('get_post_request_product'),
            data=json.dumps(self.invalid_payload_name_not_exist),
            content_type='application/json'
        )
        self.assertEqual(response.data, {
            "message": "Verifique o nome do produto solicitado. Produto solicitado: Meia da Argentina",
            "status": 400
        })


class GetSingleRequestProductTest(TestCase):
    """ Modulos de teste de pedidos para GET unico """

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')

        self.barcelona = RequestProduct.objects.create(
            product='Camiseta do Barcelona',
            unity_value_request=500,
            quantity_product_request=10,
            requester="User",
            forwarding_agent="Correios",
            address="Avenida Paulista, 4093 São Paulo-SP",
            order_status="Enviado"
        )

        self.inter = RequestProduct.objects.create(
            product='Camiseta do Inter',
            unity_value_request=300,
            quantity_product_request=19,
            requester="User",
            forwarding_agent="Avião",
            address="Avenida Faria Lima, 5000 São Paulo-SP",
            order_status="Pendente"
        )

    def test_get_valid_single_product(self):
        client.force_authenticate(user=self.admin)
        response = client.get(
            reverse('get_delete_update_request_product',
                    kwargs={'pk': self.inter.pk})
        )
        request_product = RequestProduct.objects.get(pk=self.inter.pk)
        serializer = RequestProductSerializer(request_product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        response = client.get(
            reverse('get_delete_update_request_product', kwargs={'pk': 30}))
        self.assertEqual(response.data, {
            'message': 'Não existe um pedido de registro com o ID: 30.',
            'status': 404
        })


class DeleteSingleProductTest(TestCase):
    """ Teste de deleção de pedido """

    def setUp(self):
        self.admin = User.objects.create_superuser(
            'myuser', 'admin@mgmail.com', 'test')

        self.barcelona = RequestProduct.objects.create(
            product='Camiseta do Barcelona',
            unity_value_request=500,
            quantity_product_request=10,
            requester="User",
            forwarding_agent="Correios",
            address="Avenida Paulista, 4093 São Paulo-SP",
            order_status="Enviado"
        )

        self.inter = RequestProduct.objects.create(
            product='Camiseta do Inter',
            unity_value_request=300,
            quantity_product_request=19,
            requester="User",
            forwarding_agent="Avião",
            address="Avenida Faria Lima, 5000 São Paulo-SP",
            order_status="Pendente"
        )

    def test_valid_delete_product(self):
        response = client.delete(
            reverse('get_delete_update_request_product', kwargs={'pk': self.inter.pk}))
        self.assertEqual(response.data, {
            "message": "Pedido do produto: Camiseta do Inter, deletado com sucesso no sistema.",
            "status": 204
        })

    def test_invalid_delete_product(self):
        client.force_authenticate(user=self.admin)
        response = client.delete(
            reverse('get_delete_update_request_product', kwargs={'pk': 30}))
        self.assertEqual(response.data, {
            "message": "Não existe um pedido de registro com o ID: 30.",
            "status": 404
        })
