from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'indiandelights.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'apps.home.views.home_page', name='home_page'),
    url(r'^admin/', include(admin.site.urls)),
)
