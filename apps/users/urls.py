from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^welcome/?$', views.index, name="home"),
    url(r'^register/?$', views.register, name="register"),
    url(r'^signin/?$', views.signin, name="signin"),
    url(r'^register/submit/?$', views.submit_register, name="submit_register"),
    url(r'^signin/submit/?$', views.submit_signin, name="submit_signin"),
    url(r'^logout/?$', views.logout, name="logout"),
    url(r'^dashboard/?$', views.dashboard, name="dashboard"),
    #url(r'^.+$', views.invalid),
]