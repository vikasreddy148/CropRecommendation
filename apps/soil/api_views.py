from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.farms.models import Field

from .models import SoilData
from .serializers import SoilDataSerializer
from .services import SoilDataService


class SoilDataListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SoilDataSerializer

    def get_queryset(self):
        queryset = SoilData.objects.filter(field__farm__user=self.request.user).select_related('field', 'field__farm')
        field_id = self.request.query_params.get('field')
        if field_id:
            queryset = queryset.filter(field_id=field_id)
        return queryset.order_by('-timestamp')

    def perform_create(self, serializer):
        soil_data = serializer.save()
        field = soil_data.field
        if soil_data.ph is not None:
            field.soil_ph = soil_data.ph
        if soil_data.moisture is not None:
            field.soil_moisture = soil_data.moisture
        if soil_data.n is not None:
            field.n_content = soil_data.n
        if soil_data.p is not None:
            field.p_content = soil_data.p
        if soil_data.k is not None:
            field.k_content = soil_data.k
        field.save()


class SoilDataDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SoilDataSerializer

    def get_queryset(self):
        return SoilData.objects.filter(field__farm__user=self.request.user).select_related('field', 'field__farm')


class SoilDataFetchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        field_id = request.data.get('field')
        source = request.data.get('source', 'auto')

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
                {'detail': 'Field or farm location is required to fetch soil data.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        soil_data = SoilDataService.get_soil_data(lat, lon, source)
        if not soil_data:
            return Response({'detail': 'Failed to fetch soil data.'}, status=status.HTTP_502_BAD_GATEWAY)

        is_valid, error_msg = SoilDataService.validate_soil_data(soil_data)
        if not is_valid:
            return Response({'detail': error_msg}, status=status.HTTP_400_BAD_REQUEST)

        soil_record = SoilData.objects.create(
            field=field,
            ph=soil_data.get('ph'),
            moisture=soil_data.get('moisture'),
            n=soil_data.get('n'),
            p=soil_data.get('p'),
            k=soil_data.get('k'),
            source=soil_data.get('source', 'satellite'),
        )

        if soil_record.ph is not None:
            field.soil_ph = soil_record.ph
        if soil_record.moisture is not None:
            field.soil_moisture = soil_record.moisture
        if soil_record.n is not None:
            field.n_content = soil_record.n
        if soil_record.p is not None:
            field.p_content = soil_record.p
        if soil_record.k is not None:
            field.k_content = soil_record.k
        field.save()

        return Response(SoilDataSerializer(soil_record).data, status=status.HTTP_201_CREATED)
