from django.urls import path
from dataloader import views


urlpatterns = [
    path('', views.file_uploader, name='start_page'),
    path('upload', views.upload_file, name='ajax_file_upload'),
]
