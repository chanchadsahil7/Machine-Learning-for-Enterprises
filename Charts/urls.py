from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^home/$', views.home,name="home"),
    url(r'^tables/$',views.tables,name="tables"),
    url(r'^superadmin_data/$',views.superadmin_data, name="superadmin_data"),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^upload/$', views.file_upload, name='upload'),
    url(r'^data_cleaning/$', views.data_cleaning, name='data_cleaning'),
    url(r'^to_charts/$', views.to_charts, name='to_charts'),
    url(r'^gen_charts/$', views.gen_charts, name='gen_charts'),
    url(r'^users/$', views.users, name='users'),
    url(r'^remove_user/$', views.remove_user, name='remove_user'),
]




