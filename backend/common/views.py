from django.db import connection
from django.db.utils import OperationalError
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from common.responses.api_response import ApiResponse


class HealthDataSerializer(serializers.Serializer):
    service = serializers.CharField()
    status = serializers.CharField()
    database = serializers.CharField()


class HealthResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = HealthDataSerializer()


class HealthCheckView(GenericAPIView):
    """Public endpoint used to verify API and database connectivity."""

    serializer_class = HealthResponseSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        database_status = 'connected'
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
        except OperationalError:
            database_status = 'unavailable'

        return ApiResponse.success(
            {
                'service': 'TaskVerse API',
                'status': 'ok',
                'database': database_status,
            },
            'Health check completed successfully.',
        )

