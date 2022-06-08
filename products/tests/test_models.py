from django.test import TestCase
from ..models import Product, RequestProduct

class ProductModelTest(TestCase):
    """ Esse modulo testa o Product Model """
    
    def setUp(self):
        Product.objects.create(
            name='Camiseta do Barcelona', unity_value=500, quantity_product=10, status="Pendente de envio"
        )
        Product.objects.create(
            name='Calça do Corinthians', unity_value=150, quantity_product=18, status="Enviado"
        )
        
    def test_product_model(self):
        name_product_camisa_barcelona = Product.objects.get(name='Camiseta do Barcelona')
        name_product_calca_corinthians = Product.objects.get(name='Calça do Corinthians')
        
        self.assertEqual(
            name_product_camisa_barcelona.get_product(), 'Camiseta do Barcelona adicionado com sucesso.'
        )
        
        self.assertEqual(
            name_product_calca_corinthians.get_product(), 'Calça do Corinthians adicionado com sucesso.'
        )
        
        
class RequestProductModelTest(TestCase):
    """ Esse modulo testa o Product Model """
    
    def setUp(self):
        RequestProduct.objects.create(
            product='Camiseta do Barcelona', 
            unity_value_request=500, 
            quantity_product_request=10, 
            requester="João Bortolosso", 
            forwarding_agent="Correios", 
            address="Rua dos Jabutis, 306 Jardim do Engenho 06733-019 Cotia-SP", 
            order_status="Pendente envio"
        )
        
    def test_request_model(self):
        name_request_camisa_barcelona = RequestProduct.objects.get(product='Camiseta do Barcelona')
        
        self.assertEqual(
            name_request_camisa_barcelona.get_request_product(), 'Camiseta do Barcelona solicitação enviada com sucesso.'
        )
        