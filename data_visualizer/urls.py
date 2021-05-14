from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from data_visualizer import views

app_name = 'data_visualizer'

urlpatterns = [
    url(r'^statistics$', views.statistics, name='statistics'),
    url(r'^dataset_statistics$', views.dataset_statistics, name='dataset_statistics'),
]
