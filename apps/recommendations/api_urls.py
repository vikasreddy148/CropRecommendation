from django.urls import path

from .api_views import (
    RecommendationDetailAPIView,
    RecommendationForFieldAPIView,
    RecommendationListAPIView,
    RecommendationRequestAPIView,
)

urlpatterns = [
    path('recommendations/', RecommendationListAPIView.as_view(), name='api_recommendation_list'),
    path('recommendations/request/', RecommendationRequestAPIView.as_view(), name='api_recommendation_request'),
    path('recommendations/field/<int:field_pk>/', RecommendationForFieldAPIView.as_view(), name='api_recommendation_for_field'),
    path('recommendations/<int:pk>/', RecommendationDetailAPIView.as_view(), name='api_recommendation_detail'),
]
