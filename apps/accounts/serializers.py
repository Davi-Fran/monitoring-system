from rest_framework import serializers

from apps.accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "photo",
            "email",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True},
            "last_login": {"read_only": True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)



class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "is_staff": {"required": True},
            "is_superuser": {"required": True},
            "password": {"required": True, "write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class BasicUserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "photo",
            "email",
        ]