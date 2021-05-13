from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'fileLoader'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^filelist$', views.filelist, name='filelist'),
    url(r'^dataprocess$', views.dataprocess, name='dataprocess'),
    url(r'^statistics$', views.statistics, name='statistics'),
    url(r'^chartjs$', views.chartjs, name='chartjs'),
    path('admin/', admin.site.urls),
]
