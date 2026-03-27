from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.farms.models import Field
from apps.weather.models import WeatherData

from .models import Recommendation
from .serializers import RecommendationSerializer
from .services import CropRecommendationService


def _build_reasoning(rec):
    reasoning_data = {
        'reasons': rec.get('reasons', []),
        'match_details': rec.get('match_details', {}),
    }
    if 'profit_details' in rec:
        reasoning_data['profit_details'] = rec['profit_details']
    if 'sustainability_details' in rec:
        reasoning_data['sustainability_details'] = rec['sustainability_details']
    if 'rotation_analysis' in rec:
        reasoning_data['rotation_analysis'] = rec['rotation_analysis']
    if 'composite_score' in rec:
        reasoning_data['composite_score'] = rec['composite_score']
    if 'composite_breakdown' in rec:
        reasoning_data['composite_breakdown'] = rec['composite_breakdown']
    if 'data_quality_warning' in rec:
        reasoning_data['data_quality_warning'] = rec['data_quality_warning']
    return reasoning_data


def _latest_weather_for_field(field):
    if field.latitude and field.longitude:
        return WeatherData.objects.filter(latitude=field.latitude, longitude=field.longitude).order_by('-date').first()
    if field.farm.latitude and field.farm.longitude:
        return WeatherData.objects.filter(
            latitude=field.farm.latitude, longitude=field.farm.longitude
        ).order_by('-date').first()
    return None


def _save_recommendations_for_user(user, field, generated_recommendations):
    saved_items = []
    for rec in generated_recommendations[:5]:
        existing = (
            Recommendation.objects.filter(user=user, field=field, crop_name=rec['crop_name'])
            .order_by('-created_at')
            .first()
        )
        if existing:
            existing.confidence_score = rec['confidence_score']
            existing.expected_yield = rec['expected_yield']
            existing.profit_margin = rec['profit_margin']
            existing.sustainability_score = rec['sustainability_score']
            existing.reasoning = _build_reasoning(rec)
            existing.save()
            saved_items.append(existing)
        else:
            saved_items.append(
                Recommendation.objects.create(
                    user=user,
                    field=field,
                    crop_name=rec['crop_name'],
                    confidence_score=rec['confidence_score'],
                    expected_yield=rec['expected_yield'],
                    profit_margin=rec['profit_margin'],
                    sustainability_score=rec['sustainability_score'],
                    reasoning=_build_reasoning(rec),
                )
            )
    return saved_items


class RecommendationListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecommendationSerializer

    def get_queryset(self):
        queryset = Recommendation.objects.filter(user=self.request.user).select_related('field', 'field__farm')
        field_id = self.request.query_params.get('field')
        if field_id:
            queryset = queryset.filter(field_id=field_id)
        return queryset.order_by('-created_at')[:50]


class RecommendationDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecommendationSerializer

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user).select_related('field', 'field__farm')


class RecommendationRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        field_id = request.data.get('field')
        include_weather = bool(request.data.get('include_weather', True))

        if not field_id:
            return Response({'detail': 'field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        field = get_object_or_404(Field, pk=field_id, farm__user=request.user)
        weather_data = _latest_weather_for_field(field) if include_weather else None

        generated = CropRecommendationService.get_recommendation_for_field(field=field, weather_data=weather_data, limit=10)
        if not generated:
            return Response(
                {'detail': 'No recommendations available. Please ensure field has soil data.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        saved = _save_recommendations_for_user(request.user, field, generated)
        return Response(
            {
                'field': {'id': field.id, 'name': field.name},
                'generated': generated,
                'saved': RecommendationSerializer(saved, many=True).data,
            }
        )


class RecommendationForFieldAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, field_pk):
        field = get_object_or_404(Field, pk=field_pk, farm__user=request.user)
        weather_data = _latest_weather_for_field(field)
        generated = CropRecommendationService.get_recommendation_for_field(field=field, weather_data=weather_data, limit=10)
        if not generated:
            return Response({'detail': 'No recommendations available for this field.'}, status=status.HTTP_400_BAD_REQUEST)
        saved = _save_recommendations_for_user(request.user, field, generated)
        return Response(
            {
                'field': {'id': field.id, 'name': field.name},
                'generated': generated,
                'saved': RecommendationSerializer(saved, many=True).data,
            }
        )
