from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^api/v1/products/(?P<pk>[0-9]+)$',
        views.get_delete_update_product,
        name='get_delete_update_product'
    ),
    url(
        r'^api/v1/products/$',
        views.get_post_product,
        name='get_post_product'
    )
]
