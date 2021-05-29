from django.conf.urls import url
from . import views

app_name = 'data_processor'

urlpatterns = [
    url('^form_dataset_process$', views.dataset_process, name='upload_dataset_process'),
    url(r'^dataset_process$', views.dataset_process, name='dataset_process'),
    url('^form_dataprocess/(?P<file_name>.+)$', views.dataprocess, name='upload_dataprocess'),
    url(r'^dataprocess/(?P<file_name>.+)$', views.dataprocess, name='dataprocess'),
    url(r'^process_result$', views.process_result, name='process_result'),
]
