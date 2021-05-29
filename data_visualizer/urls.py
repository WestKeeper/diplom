from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from data_visualizer import views

app_name = 'data_visualizer'

urlpatterns = [
    url(r'^dataset_stat$', views.dataset_stat, name='dataset_stat'),
    url(r'^statistics/(?P<file_path>.+)', views.statistics, name='statistics'),
    url(r'^processed_statistics/(?P<file_path>.+)', views.processed_statistics, name='processed_statistics'),
]
