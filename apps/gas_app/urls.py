"""
Define URLs for gas app, namespace: `gas`
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^cars/new/?$', views.new_car, name="new_car"),
    url(r'^cars/create$', views.create_car, name="create_car"),
    url(r'^cars/(?P<car_id>\d+)/?$', views.view_car, name="view_car"),
    url(r'^cars/edit/(?P<car_id>\d+)/?$', views.edit_car, name="edit_car"),
    url(r'^cars/update$', views.update_car, name="update_car"),
    url(r'^cars/delete/(?P<car_id>\d+)/?$', views.delete_car, name="delete_car"),
    url(r'^entries/new/?$', views.new_entry, name="new_entry"),
    url(r'^entries/create$', views.create_entry, name="create_entry"),
    url(r'^entries/(?P<entry_id>\d+)/?$', views.view_entry, name="view_entry"),
    url(r'^entries/edit/(?P<entry_id>\d+)/?$', views.edit_entry, name="edit_entry"),
    url(r'^entries/update(?P<entry_id>\d+)/?$', views.update_entry, name="update_entry"),
    url(r'^entries/delete$', views.delete_entry, name="delete_entry"),
]
