from django.conf.urls import url
from . import views

app_name = 'report_controller'

urlpatterns = [
    url(r'^dataset_report$', views.dataset_report, name='dataset_report'),
    url(r'^report_result/(?P<file_path>.+)', views.report_result, name='report_result'),
    url(r'^processed_report_result/(?P<file_path>.+)', views.processed_report_result, name='processed_report_result')
]
