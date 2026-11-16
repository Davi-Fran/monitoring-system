from django.db import transaction

from rest_framework import viewsets

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)

from apps.devices.serializers import (
    MicroControllerModelSerializer,
    MicroControllerSerializer,
    MicroControllerDetailSerializer,
)

from apps.devices.selectors import (
    micro_controller_model_list, 
    micro_controller_list,
    micro_controller_retrieve
)


@extend_schema(tags=["Micro Controller Models"])
@extend_schema_view(
    list=extend_schema(
        summary="List all micro controller models",
        parameters=[
            OpenApiParameter(
                "is_active",
                str,
                enum=["true", "false"],
                description="Filters by micro controller model status. Without that, list them all.",
            ),
        ],
    ),
    create=extend_schema(summary="Creates a new micro controller model"),
    retrieve=extend_schema(summary="Gets a specific micro controller model"),
    partial_update=extend_schema(summary="Edit micro controller model data",)
)
class MicroControllerModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        if self.action == "list":
            return micro_controller_model_list(filters=self.request.query_params)

        return micro_controller_model_list()

    def get_serializer_class(self):
        return MicroControllerModelSerializer
    

@extend_schema(tags=["Micro Controllers"])
@extend_schema_view(
    list=extend_schema(
        summary="List all micro controllers",
        parameters=[
            OpenApiParameter(
                "is_active",
                str,
                enum=["true", "false"],
                description="Filters by micro controller status. Without that, list them all."
            ),
        ],
    ),
    create=extend_schema(
        summary="Creates a new micro controller",
        description="You can't create a micro controller with a model or a lab that's currently inactive",
    ),
    retrieve=extend_schema(summary="Gets a specific micro controller"),
    partial_update=extend_schema(
        summary="Edit micro controller data",
        description="When you inactivate a micro controller, its sensors are also inactivated.",
    ),
)
class MicroControllerViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        if self.action == "list":
            return micro_controller_list(filters=self.request.query_params)
        elif self.action == "retrieve":
            return micro_controller_retrieve()

        return micro_controller_list()


    def get_serializer_class(self):
        if self.action == "retrieve":
            return MicroControllerDetailSerializer

        return MicroControllerSerializer

    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()