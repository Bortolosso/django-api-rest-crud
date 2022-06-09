from django.conf.urls import url
from . import views

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^docs/', schema_view),
    url(
        r'^api/v1/products/(?P<pk>[0-9]+)$',
        views.get_delete_update_product,
        name='get_delete_update_product'
    ),
    url(
        r'^api/v1/products/$',
        views.get_post_product,
        name='get_post_product'
    ),
    url(
        r'^api/v1/request/products/$',
        views.get_post_request_product,
        name='get_post_request_product'
    ),
    url(
        r'^api/v1/request/products/(?P<pk>[0-9]+)$',
        views.get_delete_update_request_product,
        name='get_delete_update_request_product'
    )
]
