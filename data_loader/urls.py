from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'data_loader'

urlpatterns = [
    url('upload', views.filelist, name='upload_filelist'),
    url(r'^$', views.filelist, name='filelist'),
    url(r'^dataset/(?P<file_path>.+)', views.dataset, name='dataset'),
    url(r'^processed_dataset/(?P<file_path>.+)', views.processed_dataset, name='processed_dataset'),
]