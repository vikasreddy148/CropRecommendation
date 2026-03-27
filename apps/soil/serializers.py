from rest_framework import serializers

from apps.farms.models import Field

from .models import SoilData


class SoilDataSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.name', read_only=True)
    farm_name = serializers.CharField(source='field.farm.name', read_only=True)

    class Meta:
        model = SoilData
        fields = [
            'id',
            'field',
            'field_name',
            'farm_name',
            'ph',
            'moisture',
            'n',
            'p',
            'k',
            'source',
            'timestamp',
        ]

    def validate_field(self, value):
        request = self.context.get('request')
        if request and value.farm.user_id != request.user.id:
            raise serializers.ValidationError('Invalid field selected.')
        return value
