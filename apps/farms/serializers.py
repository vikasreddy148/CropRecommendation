from decimal import Decimal

from django.db.models import Sum
from rest_framework import serializers

from .models import Farm, Field


class FarmSerializer(serializers.ModelSerializer):
    field_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Farm
        fields = [
            'id',
            'name',
            'latitude',
            'longitude',
            'area',
            'soil_type',
            'field_count',
            'created_at',
            'updated_at',
        ]


class FieldSerializer(serializers.ModelSerializer):
    farm_name = serializers.CharField(source='farm.name', read_only=True)

    class Meta:
        model = Field
        fields = [
            'id',
            'farm',
            'farm_name',
            'name',
            'latitude',
            'longitude',
            'area',
            'soil_ph',
            'soil_moisture',
            'n_content',
            'p_content',
            'k_content',
            'last_updated',
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        farm = attrs.get('farm') or getattr(self.instance, 'farm', None)
        area = attrs.get('area') or getattr(self.instance, 'area', None)

        if not farm or not user:
            return attrs

        if farm.user_id != user.id:
            raise serializers.ValidationError({'farm': 'Invalid farm selected.'})

        if area is not None:
            existing_fields = farm.fields.exclude(pk=getattr(self.instance, 'pk', None))
            total_existing_area = existing_fields.aggregate(total=Sum('area'))['total'] or Decimal('0.00')
            total_area = total_existing_area + Decimal(str(area))
            if total_area > farm.area:
                available_area = farm.area - total_existing_area
                raise serializers.ValidationError(
                    {
                        'area': (
                            f'Total field area exceeds farm area. '
                            f'Available area: {available_area:.2f} ha.'
                        )
                    }
                )

        return attrs
