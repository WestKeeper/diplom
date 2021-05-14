from django.urls import path
from functionapplyer import views


urlpatterns = [
    path('processed', views.func_pipeline, name='func'),
]
