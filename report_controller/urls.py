from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'report_controller'

urlpatterns = [
    url(r'^report_result$', views.report_result, name='report_result'),
]
