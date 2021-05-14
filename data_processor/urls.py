from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'data_processor'

urlpatterns = [
    url(r'^dataprocess$', views.dataprocess, name='dataprocess'),
    url(r'^process_result$', views.process_result, name='process_result'),
]
