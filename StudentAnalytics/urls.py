from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

urlpatterns = [
    url(r'^', include('data_loader.urls', namespace='data_loader')),
    url(r'^', include('data_processor.urls', namespace='data_processor')),
    url(r'^', include('data_visualizer.urls', namespace='data_visualizer')),
    url(r'^', include('report_controller.urls', namespace='report_controller')),
    url(r'^', include('predict_model_controller.urls', namespace='report_controller')),
    url(r'^fileLoader/', include('fileLoader.urls',
                                 namespace='fileLoader')),
    path('admin/', admin.site.urls),
]
