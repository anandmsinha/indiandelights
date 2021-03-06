from django.conf.urls import patterns, include, url
from .views import item_by_pk, cart_manager


urlpatterns = patterns('',
    url(r'^item/(?P<pk>[0-9]+)/$', item_by_pk, name='item_pk'),
    url(r'^item/cart/$', cart_manager, name='item_cart'),
)