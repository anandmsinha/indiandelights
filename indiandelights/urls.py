from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from apps.product import urls as app_product_urls


urlpatterns = patterns('',
    url(r'^$', 'apps.home.views.home_page', name='home_page'),
    url(r'^cart/$', 'apps.product.views.cart_view', name='cart_view'),
    url(r'^item/', include(app_product_urls)),
    url(r'^site/terms/$', TemplateView.as_view(template_name='static/terms.html'), name='site_terms'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
