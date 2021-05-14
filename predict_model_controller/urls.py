from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'predict_model_controller'

urlpatterns = [
    url(r'^model_info$', views.teaching_model_info, name='model_info'),
    url(r'^model_result$', views.teaching_model_result, name='model_result'),
    url(r'^predict_form$', views.predict_form, name='predict_form'),
    url(r'^predict_result$', views.predict_result, name='predict_result'),
]
