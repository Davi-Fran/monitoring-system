from rest_framework import viewsets

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from apps.core.permissions import IsAdminOrSelf
from apps.core.permissions import is_admin
from apps.accounts.selectors import user_list
from apps.accounts.serializers import UserSerializer, CreateUserSerializer, BasicUserEditSerializer

@extend_schema(tags=["Users"])
@extend_schema_view(
    list=extend_schema(summary="List all users"),
    create=extend_schema(
        summary="Creates a new user.",
        description="Only super users can create new users"
    ),
    retrieve=extend_schema(summary="Gets a specfic user"),
    partial_update=extend_schema(
        summary="Edit user data",
        description="To edit profile photo use \"multipart/form-data\" and send the photo"
    )
)
class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        return user_list()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        if self.action == "partial_update" and not is_admin(self.request.user):
            return BasicUserEditSerializer

        return UserSerializer

    def get_permissions(self):
        if self.action == "partial_update":
            return [IsAdminOrSelf()]

        return super().get_permissions()