from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'data_loader'

urlpatterns = [
    url(r'^$', views.filelist, name='filelist'),
    url(r'^dataset$', views.dataset, name='dataset'),
]
