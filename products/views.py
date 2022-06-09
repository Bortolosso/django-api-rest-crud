from django_filters.utils import translate_validation
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import Product, RequestProduct
from .serializers import ProductSerializer, RequestProductSerializer
from .filters import ProductFilter, RequestProductFilter

"""Viwes
Views baseado em função
"""


@ api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
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
            exist_product_name = Product.objects.filter(
                name=request.data.get('name')).exists()
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
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated,  IsAdminUser])
def get_post_product(request):

    if request.method == 'GET':
        filterset = ProductFilter(request.GET, queryset=Product.objects.all())
        if not filterset.is_valid():
            raise translate_validation(filterset.errors)
        serializer = ProductSerializer(filterset.qs, many=True)
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


@ api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated,  IsAdminUser])
def get_post_request_product(request):

    if request.method == 'GET':
        filterset = RequestProductFilter(
            request.GET, queryset=RequestProduct.objects.all())
        if not filterset.is_valid():
            raise translate_validation(filterset.errors)
        serializer = RequestProductSerializer(filterset.qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        product_requested = request.data.get('product')
        if not product_requested:
            return Response({
                "message": "Payload incorreto, parametro product obrigatorio.",
                "status": status.HTTP_400_BAD_REQUEST
            })
        exist_product = Product.objects.filter(name=product_requested).exists()
        try:
            find_product_by_name = Product.objects.get(name=product_requested)
        except Exception:
            return Response({
                "message": "Verifique o nome do produto solicitado. Produto solicitado: {0}".format(product_requested),
                "status": status.HTTP_400_BAD_REQUEST
            })
            
        quantity_product_by_get = find_product_by_name.quantity_product
        status_product_by_get = find_product_by_name.status
        request_solicited = request.data.get('quantity_product_request')
        quantity_product = quantity_product_by_get - request_solicited
        status_product = "Indisponivel"
        if quantity_product > 0:
            status_product = "Disponivel"

        if request_solicited > quantity_product_by_get:
            return Response({
                "message": "A quantidade de itens é maior do que disponível em estoque. Solicitado: {0}, Disponivel: {1}.".format(request_solicited, quantity_product_by_get),
                "status": status.HTTP_400_BAD_REQUEST
            })

        if not exist_product:
            return Response({
                "message": "Produto: {0}, não exites no sistema.".format(product_requested),
                "status": status.HTTP_400_BAD_REQUEST
            })

        if status_product_by_get == "Indisponivel":
            return Response({
                "message": "Produto: {0}, não está disponível no sistema.".format(product_requested),
                "status": status.HTTP_400_BAD_REQUEST
            })

        data_product = {
            'id': find_product_by_name.id,
            'name': find_product_by_name.name,
            'unity_value': find_product_by_name.unity_value,
            'quantity_product': quantity_product,
            'status': status_product,
        }

        data_request = {
            'product': request.data.get('product'),
            'unity_value_request': int(request.data.get('unity_value_request')),
            'quantity_product_request': int(request.data.get('quantity_product_request')),
            'requester': request.data.get('requester'),
            'forwarding_agent': request.data.get('forwarding_agent'),
            'address': request.data.get('address'),
            'order_status': request.data.get('order_status'),
        }

        serializer_update_product = ProductSerializer(
            find_product_by_name, data=data_product)
        serializer_request_product = RequestProductSerializer(
            data=data_request)

        if serializer_update_product.is_valid() and serializer_request_product.is_valid():
            serializer_request_product.save()
            serializer_update_product.save()

            return Response({
                "message": "Solicitação do pedido {0} envidada com sucesso.".format(request.data.get('product')),
                "data_product_updated": serializer_update_product.data,
                "data_request_product": serializer_request_product.data,
                "status": status.HTTP_201_CREATED
            })

        return Response({
            "message": "verifique seu object payload.",
            "data": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


@ api_view(['GET', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_delete_update_request_product(request, pk):
    try:
        request_product = RequestProduct.objects.get(pk=pk)
    except RequestProduct.DoesNotExist:
        return Response({
            "message": "Não existe um pedido de registro com o ID: {0}.".format(pk),
            "status": status.HTTP_404_NOT_FOUND
        })

    if request.method == 'GET':
        serializer = RequestProductSerializer(request_product)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        request_product.delete()
        return Response({
            "message": "Pedido do produto: {0}, deletado com sucesso no sistema.".format(request_product.product),
            "status": status.HTTP_204_NO_CONTENT
        })
