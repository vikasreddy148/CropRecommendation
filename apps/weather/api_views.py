from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.farms.models import Field

from .models import WeatherData
from .serializers import WeatherDataSerializer
from .services import WeatherDataService


class WeatherDataListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WeatherDataSerializer

    def get_queryset(self):
        return WeatherData.objects.all().order_by('-date', '-created_at')[:100]


class WeatherDataDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WeatherDataSerializer
    queryset = WeatherData.objects.all()


class WeatherDataFetchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        field_id = request.data.get('field')
        if not field_id:
            return Response({'detail': 'field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            field = Field.objects.get(pk=field_id, farm__user=request.user)
        except Field.DoesNotExist:
            return Response({'detail': 'Field not found.'}, status=status.HTTP_404_NOT_FOUND)

        if field.latitude and field.longitude:
            lat = float(field.latitude)
            lon = float(field.longitude)
        elif field.farm.latitude and field.farm.longitude:
            lat = float(field.farm.latitude)
            lon = float(field.farm.longitude)
        else:
            return Response(
                {'detail': 'Field or farm location is required for weather fetch.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_weather = WeatherDataService.fetch_openweathermap_current(lat, lon)
        if not current_weather:
            return Response({'detail': 'Failed to fetch weather data.'}, status=status.HTTP_502_BAD_GATEWAY)

        is_valid, error_msg = WeatherDataService.validate_weather_data(current_weather)
        if not is_valid:
            return Response({'detail': error_msg}, status=status.HTTP_400_BAD_REQUEST)

        weather_data, _ = WeatherData.objects.update_or_create(
            latitude=lat,
            longitude=lon,
            date=timezone.now().date(),
            defaults={
                'temperature': current_weather.get('temperature'),
                'rainfall': current_weather.get('rainfall', 0),
                'humidity': current_weather.get('humidity'),
                'wind_speed': current_weather.get('wind_speed'),
                'forecast_data': {
                    'pressure': current_weather.get('pressure'),
                    'description': current_weather.get('description'),
                    'icon': current_weather.get('icon'),
                },
            },
        )
        return Response(WeatherDataSerializer(weather_data).data)
