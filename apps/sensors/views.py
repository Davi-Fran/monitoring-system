from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)
from drf_spectacular.types import OpenApiTypes

from apps.sensors.selectors import (
    sensor_model_list,
    sensor_list,
    sensor_retrieve, 
    sensor_reading_list,
    latest_reading_list,
    offline_sensors_list,
)

from apps.sensors.serializers import (
    SensorModelSerializer, 
    SensorSerializer, 
    SensorDetailSerializer, 
    SensorReadingSerializer,
    LatestReadingSerializer,
    LatestReadingQuerySerializer,
    OfflineSensorQuerySerializer,
    OfflineSensorSerializer,
)

from apps.sensors.choices import UNIT_BY_FUNCTION


@extend_schema(tags=["Sensor Models"])
@extend_schema_view(
    list=extend_schema(
        summary="List all sensors models",
        parameters=[
            OpenApiParameter(
                "is_active",
                str,
                enum=["true", "false"],
                description="Filters by sensor model status. Without that, list them all."
            )
        ]
    ),
    create=extend_schema(summary="Creates a new sensor model"),
    retrieve=extend_schema(summary="Gets a specfic sensor model"),
    partial_update=extend_schema(summary="Edit sensor model data"),
)
class SensorModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        if self.action == "list":
            return sensor_model_list(filters=self.request.query_params)

        return sensor_model_list()

    def get_serializer_class(self):
        return SensorModelSerializer

    def perform_create(self, serializer):
        sm_function = serializer.validated_data["sm_function"]
        serializer.save(sm_measurement_unit=UNIT_BY_FUNCTION[sm_function])

    def perform_update(self, serializer):
        sm_function = serializer.validated_data.get("sm_function")

        if sm_function is not None:
            serializer.save(sm_measurement_unit=UNIT_BY_FUNCTION[sm_function])
            return

        serializer.save()



@extend_schema(tags=["Sensors"])
@extend_schema_view(
    list=extend_schema(
        summary="List all sensors",
        parameters=[
            OpenApiParameter("is_active", bool),
            OpenApiParameter("micro_controller_id", int)
        ]
    ),
    create=extend_schema(summary="Creates a new sensor"),
    retrieve=extend_schema(summary="Gets a specfic sensor"),
    partial_update=extend_schema(summary="Edit sensor data"),
    offline_sensors=extend_schema(
        summary="List all sensors that doesn't generate readings in a period",
        parameters=[OpenApiParameter("minutes", int)],
    )
)
class SensorViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        if self.action == "list":
            return sensor_list(filters=self.request.query_params)
        elif self.action == "retrieve":
            return sensor_retrieve()
    
        return sensor_list()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SensorDetailSerializer

        return SensorSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="offline-sensors",
    )
    def offline_sensors(self, request):
        query = OfflineSensorQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)

        sensors = offline_sensors_list(minutes=query.validated_data["minutes"])
        serializer = OfflineSensorSerializer(sensors, many=True)
        return Response(serializer.data)



@extend_schema(tags=["Sensor Readings"])
@extend_schema_view(
    list=extend_schema(
        summary="List all readings",
        parameters=[
            OpenApiParameter("since", OpenApiTypes.DATETIME),
            OpenApiParameter("until", OpenApiTypes.DATETIME),
            OpenApiParameter("sensor_id", int),
            OpenApiParameter("laboratory_id", int),
        ]
    ),
    create=extend_schema(summary="Creates a new reading"),
    retrieve=extend_schema(summary="Gets a specfic reading"),
    latest=extend_schema(
        summary="List the most recent reading of each sensor",
        parameters=[OpenApiParameter("last_24h", bool)]
    )
)
class SensorReadingViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        if self.action == "list":
            return sensor_reading_list(filters=self.request.query_params)

        return sensor_reading_list()

    def get_serializer_class(self):
        if self.action == "latest":
            return LatestReadingSerializer

        return SensorReadingSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="latest",
    )
    def latest(self, request):
        query = LatestReadingQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)

        latest_readings = latest_reading_list(last_24h=query.validated_data["last_24h"])
        serializer = self.get_serializer(latest_readings, many=True)
        return Response(serializer.data)