from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)/$', 'apps.product.views.item_by_pk', name='item_pk'),
    url(r'^cart/$', 'apps.product.views.cart_manager', name='item_cart'),
)