from django.conf.urls import patterns, include, url

from django.contrib import admin
from users import views
from users.models import NICK_PATTERN

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name="list"),
    url(r'^(?P<slug>{})/$'.format(NICK_PATTERN), views.UserView.as_view(), name="detail"),
    url(r'^create$', views.UserCreateView.as_view(), name="user_create"),
    url(r'^(?P<slug>{})/edit$'.format(NICK_PATTERN), views.UserUpdateView.as_view(), name="user_update"),
)
