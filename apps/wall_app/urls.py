from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^home', views.home),
    url(r'^wall$', views.wall),
    url(r'^add_message_home$', views.add_message_home),
    url(r'^add_message_wall$', views.add_message_wall),
    url(r'^add_comment/$', views.add_comment),
    url(r'^delete_wall/(?P<message_id>\d+)$', views.delete_wall),
    url(r'^delete_home/(?P<message_id>\d+)$', views.delete_home),
]