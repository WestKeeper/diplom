from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'fileLoader'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dataprocess$', views.dataprocess, name='dataprocess'),
    url(r'^statistics$', views.statistics, name='statistics'),
    url(r'^chartjs$', views.chartjs, name='chartjs'),
    url(r'^dataframe_statistics$', views.dataframe_statistics, name='dataframe_statistics'),
    url(r'^dataframe_report$', views.dataframe_report, name='dataframe_report'),
    url(r'^dataframe_teaching_model$', views.dataframe_teaching_model, name='dataframe_teaching_model'),
    url(r'^teaching_model_info$', views.teaching_model_info, name='teaching_model_info'),
    url(r'^predict_form$', views.predict_form, name='predict_form'),
    url(r'^teaching_model_result$', views.teaching_model_result, name='teaching_model_result'),
    url(r'^predict_result$', views.predict_result, name='predict_result'),
    path('admin/', admin.site.urls),
]
