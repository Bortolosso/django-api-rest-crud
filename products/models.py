from django.db import models


class Product(models.Model):
    name = models.CharField("Name", max_length=240)
    unity_value = models.IntegerField("Unity", default = 0)
    quantity_product = models.IntegerField("Quantity", default = 0)
    status = models.CharField("Status", max_length=240, default = "", blank=True)
    
    def get_product(self):
        return self.name + ' adicionado com sucesso.'

class RequestProduct(models.Model):
    product = models.CharField("Product", max_length=240)
    unity_value_request = models.IntegerField("UnityRequest", default = 0)
    quantity_product_request = models.IntegerField("QuantityRequest", default = 0)
    solicitation = models.DateTimeField(auto_now=True, blank=True)
    requester = models.CharField("Requester", max_length=240)
    forwarding_agent = models.CharField("Requester", max_length=240)
    address = models.CharField("Requester", max_length=240)
    order_status = models.CharField("Requester", max_length=240)
    
    def get_request_product(self):
        return self.product + ' solicitação enviada com sucesso.'