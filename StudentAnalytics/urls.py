from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('data_loader.urls', namespace='data_loader')),
    url(r'^', include('data_processor.urls', namespace='data_processor')),
    url(r'^', include('data_visualizer.urls', namespace='data_visualizer')),
    url(r'^', include('predict_model_controller.urls', namespace='predict_model_controller')),
    url(r'^', include('report_controller.urls', namespace='report_controller')),
]
