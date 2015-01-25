from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from apps.product import urls as app_product_urls
from apps.product import views as app_product_view
from apps.home import views as app_home_view


urlpatterns = patterns('',
    url(r'^$', app_home_view.home_page, name='home_page'),
    url(r'^vendors/$', app_home_view.vendor_view, name='vendor_view'),
    url(r'^cart/$', app_product_view.cart_view, name='cart_view'),
    url(r'^item/', include(app_product_urls)),
    url(r'^site/partners/$', TemplateView.as_view(template_name='static/partner.html'), name='site_partner'),
    url(r'^site/terms/$', TemplateView.as_view(template_name='static/terms.html'), name='site_terms'),
    url(r'^404/$', app_home_view.not_found, name='404_view'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
