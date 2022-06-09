from cmath import log
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer

"""Viwes
Views baseado em função
"""


@ api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({
            "message": "Não existe registro com o ID: {0}.".format(pk), 
            "status": status.HTTP_404_NOT_FOUND
        })

    if request.method == 'GET':
        serializer = ProductSerializer(product)

        return Response(serializer.data)

    elif request.method == 'DELETE':
        product.delete()

        return Response({
            "message": "Produto: {0}, deletado com sucesso no sistema.".format(product.name), 
            "status": status.HTTP_204_NO_CONTENT
        })

    elif request.method == 'PUT':
        name_product = request.data.get('name')
        quantity_product = int(request.data.get('quantity_product'))
        
        if request.data.get('name') != product.name:  
            exist_product_name = Product.objects.filter(name=request.data.get('name')).exists()

            if exist_product_name:
                return Response({
                    "message": "Já existe um produto com o nome: {0}".format(name_product), 
                    "data": request.data, 
                    "status": status.HTTP_400_BAD_REQUEST
                })

        status_product = "Indisponivel"
        if quantity_product > 0:
            status_product = "Disponivel"

        data = {
            'id': pk,
            'name': name_product,
            'unity_value': int(request.data.get('unity_value')),
            'quantity_product': quantity_product,
            'status': status_product,
        }
        serializer = ProductSerializer(product, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Produto atualizado com sucesso. ID: {0}".format(pk), 
                "data": serializer.data, 
                "status": status.HTTP_204_NO_CONTENT
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET', 'POST'])
def get_post_product(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        name_product = request.data.get('name')
        quantity_product = int(request.data.get('quantity_product'))

        status_product = "Indisponivel"
        if quantity_product > 0:
            status_product = "Disponivel"

        exist_product_name = Product.objects.filter(
            name=request.data.get('name')).exists()
        if exist_product_name:
            return Response({
                "message": "Produto: {0}, já cadastrado no sistema.".format(name_product),
                "status": status.HTTP_400_BAD_REQUEST
            })

        data = {
            'name': name_product,
            'unity_value': int(request.data.get('unity_value')),
            'quantity_product': quantity_product,
            'status': status_product,
        }
        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Produto adicioando com sucesso.",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED
            })

        return Response({
            "message": "verifique seu object payload.",
            "data": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })
