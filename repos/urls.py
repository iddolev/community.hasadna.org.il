from django.conf.urls import patterns, include, url

from django.contrib import admin
from repos import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name="list"),
    url(r'^(?P<pk>\d+)/$', views.ProjectView.as_view(), name="project_detail"),
    url(r'^create$', views.ProjectCreateView.as_view(), name="project_create"),
    url(r'^(?P<pk>\d+)/edit$', views.ProjectUpdateView.as_view(), name="project_update"),
    url(r'^(?P<pk>\d+)/add_repo$', views.add_repo, name="add_repo"),
)
