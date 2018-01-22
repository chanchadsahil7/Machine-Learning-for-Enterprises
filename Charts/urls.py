from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^home/$', views.home,name="home"),
    url(r'^superadmin/$',views.super_user,name="superadmin"),
    url(r'^superadmin_data/$',views.superadmin_data, name="superadmin_data"),
    url(r'^upload/$',views.simple_upload, name="upload"),
    url(r'^logout/$', views.logout, name='logout'),
]