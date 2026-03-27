from django.urls import path

from .api_views import WeatherDataDetailAPIView, WeatherDataFetchAPIView, WeatherDataListCreateAPIView

urlpatterns = [
    path('weather/', WeatherDataListCreateAPIView.as_view(), name='api_weather_list_create'),
    path('weather/<int:pk>/', WeatherDataDetailAPIView.as_view(), name='api_weather_detail'),
    path('weather/fetch/', WeatherDataFetchAPIView.as_view(), name='api_weather_fetch'),
]
