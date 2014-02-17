from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'choi.views.home', name='home'),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^projects/', include('repos.urls', namespace='repos')),
    url(r'^admin/', include(admin.site.urls)),
)
