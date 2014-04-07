from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from users import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$',  TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^projects/', include('repos.urls', namespace='repos')),
    url(r'^skills/$',  views.skills, name='skills'),
    url(r'^skills/(\w+)/$',  views.skill_by_slug, name='skill_by_slug'),
    url(r'^admin/', include(admin.site.urls)),
)
