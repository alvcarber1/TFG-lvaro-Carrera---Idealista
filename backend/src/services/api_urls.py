from django.urls import path
from . import api_views

urlpatterns = [
    path('properties/', api_views.PropertyListAPIView.as_view(), name='api-properties'),
    path('clustering/', api_views.ClusteringAPIView.as_view(), name='api-clustering'),
    path('predict/', api_views.PredictAPIView.as_view(), name='api-predict'),
]