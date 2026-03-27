from rest_framework import serializers

from .models import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.name', read_only=True)
    farm_name = serializers.CharField(source='field.farm.name', read_only=True)

    class Meta:
        model = Recommendation
        fields = [
            'id',
            'field',
            'field_name',
            'farm_name',
            'crop_name',
            'confidence_score',
            'expected_yield',
            'profit_margin',
            'sustainability_score',
            'reasoning',
            'created_at',
        ]
