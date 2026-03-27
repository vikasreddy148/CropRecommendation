from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from .models import Farm, Field
from .serializers import FarmSerializer, FieldSerializer


class FarmListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FarmSerializer

    def get_queryset(self):
        return (
            Farm.objects.filter(user=self.request.user)
            .annotate(field_count=Count('fields'))
            .order_by('-created_at')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FarmRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FarmSerializer

    def get_queryset(self):
        return Farm.objects.filter(user=self.request.user).annotate(field_count=Count('fields'))


class FieldListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FieldSerializer

    def get_queryset(self):
        queryset = Field.objects.filter(farm__user=self.request.user).select_related('farm').order_by('farm', 'name')
        farm_id = self.request.query_params.get('farm')
        if farm_id:
            queryset = queryset.filter(farm_id=farm_id)
        return queryset


class FieldRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FieldSerializer

    def get_queryset(self):
        return Field.objects.filter(farm__user=self.request.user).select_related('farm')
