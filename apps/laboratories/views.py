from django.db import transaction

from rest_framework import viewsets

from drf_spectacular.utils import (
    extend_schema, 
    extend_schema_view,
    OpenApiParameter,
)

from apps.laboratories.serializers import LaboratorySerializer, LaboratoryDetailSerializer
from apps.laboratories.selectors import laboratory_list, laboratory_retrieve


@extend_schema(tags=["Laboratories"])
@extend_schema_view(
    list=extend_schema(
        summary="List all laboratories",
        parameters=[
            OpenApiParameter(
                "is_active",
                str,
                enum=["true", "false"],
                description="Filters by lab status. Without that, list them all."
            ),
        ],
    ),
    create=extend_schema(summary="Creates a new laboratory"),
    retrieve=extend_schema(summary="Gets a specific laboratory"),
    partial_update=extend_schema(
        summary="Edit laboratory data",
        description="When you inactivate a laboratory, its micro controllers and sensors are also inactivated.",
    ),
)
class LaboratoryViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        if self.action == "list":
            return laboratory_list(filters=self.request.query_params)
        elif self.action == "retrieve":
            return laboratory_retrieve()

        return laboratory_list()


    def get_serializer_class(self):
        if self.action == "retrieve":
            return LaboratoryDetailSerializer

        return LaboratorySerializer


    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()