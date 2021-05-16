from django.urls import path
from predict_model import views


urlpatterns = [
    path('ml_model', views.svc_model, name='ML_model_page'),
    # path('ml_model_train', views.svc_model, name='ML_model_train'),
    # path('ml_model_predict', views.svc_model, name='ML_model_predict'),
]
