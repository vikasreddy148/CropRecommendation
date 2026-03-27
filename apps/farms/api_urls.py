from django.urls import path

from .api_views import (
    FarmListCreateAPIView,
    FarmRetrieveUpdateDestroyAPIView,
    FieldListCreateAPIView,
    FieldRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('farms/', FarmListCreateAPIView.as_view(), name='api_farm_list_create'),
    path('farms/<int:pk>/', FarmRetrieveUpdateDestroyAPIView.as_view(), name='api_farm_detail'),
    path('fields/', FieldListCreateAPIView.as_view(), name='api_field_list_create'),
    path('fields/<int:pk>/', FieldRetrieveUpdateDestroyAPIView.as_view(), name='api_field_detail'),
]
