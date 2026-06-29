from rest_framework import serializers

from ..serializers.permission_serializer import PermissionSerializer
from ..serializers.role_serializer import RoleMiniSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=150, required=False)
    email_or_username = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(write_only=True)
    roles = RoleMiniSerializer(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def to_internal_value(self, data):
        email = data.get("email")
        username = data.get("username")
        if not email and not username:
            raise serializers.ValidationError(
                {
                    "non_field_errors": "Either email or username must be provided."
                }
            )
        
        mutable_data = data.copy()

        mutable_data["email_or_username"] = email if email else username

        return self.to_internal_value(mutable_data)

    def get_permissions(self, obj):
        user = self.context.get("user")
        permissions = user.get_all_permissions()

        grouped_data = {}

        for perm in permissions:
            if perm.content_type.name not in grouped_data:
                grouped_data[perm.content_type.name] = []
            grouped_data[perm.content_type.name].append(perm.codename)

        formatted_list = [
            {"module": module, "actions": actions}
            for module, actions in grouped_data.items()
        ]

        return PermissionSerializer(
            formatted_list,
            many=True
        ).data


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=150, required=False)
    email_or_username = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=128)

    def to_internal_value(self, data):
        email = data.get("email")
        username = data.get("username")
        if not email and not username:
            raise serializers.ValidationError(
                {
                    "non_field_errors": "Either email or username must be provided."
                }
            )
        
        mutable_data = data.copy()

        mutable_data["email_or_username"] = email if email else username

        return self.to_internal_value(mutable_data)

    def validate_email(self, attr):
        if User.objects.filter(
            email=attr,
        ).exists():
            raise serializers.ValidationError(
                "User with this email already exists."
            )
        
        return attr
    
    def validate_username(self, attr):
        if User.objects.filter(
            username=attr,
        ).exists():
            raise serializers.ValidationError(
                "User with this username already exists."
            )
        
        return attr
    

class GoogleSerializer(serializers.Serializer):
    code = serializers.CharField()
