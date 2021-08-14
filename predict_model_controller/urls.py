from django.conf.urls import url
from . import views

app_name = 'predict_model_controller'

urlpatterns = [
    url(r'^svc_model/(?P<file_path>.+)', views.svc_model, name='svc_model'),
    url(r'^dataset_teaching_model$', views.dataset_teaching_model, name='dataset_teaching_model'),
    url(r'^predict_form_upload$', views.predict_form, name='predict_form_upload'),
    url(r'^predict_form$', views.predict_form, name='predict_form'),
    url(r'^model_data_upload$', views.predict_form, name='model_data_upload'),
    url(r'^predict_result$', views.predict_result, name='predict_result'),
]
