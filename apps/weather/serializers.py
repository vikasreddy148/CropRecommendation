from rest_framework import serializers

from .models import WeatherData


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = [
            'id',
            'latitude',
            'longitude',
            'date',
            'temperature',
            'rainfall',
            'humidity',
            'wind_speed',
            'forecast_data',
            'created_at',
            'updated_at',
        ]
