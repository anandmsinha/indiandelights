from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import register


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='static/partner.html'), name='index'),
    url(r'^register/$', register, name='register'),
    url(r'^thank-you/$', TemplateView.as_view(template_name='partners/thankyou.html'), name='thanks')
)