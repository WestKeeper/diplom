from django.urls import path
from predict_model import views


urlpatterns = [
    path('/ml_model', views.svc_model, name='ML_model_page'),
]
