from django.urls import path

from .api_views import SoilDataDetailAPIView, SoilDataFetchAPIView, SoilDataListCreateAPIView

urlpatterns = [
    path('soil/', SoilDataListCreateAPIView.as_view(), name='api_soil_list_create'),
    path('soil/<int:pk>/', SoilDataDetailAPIView.as_view(), name='api_soil_detail'),
    path('soil/fetch/', SoilDataFetchAPIView.as_view(), name='api_soil_fetch'),
]
