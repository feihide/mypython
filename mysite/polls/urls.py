from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('get',views.apiGet),
    url('one',views.apiOne),
    url('del',views.apiDel),
    url('favor',views.apiFavor),
]
