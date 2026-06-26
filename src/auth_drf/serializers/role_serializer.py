from rest_framework import serializers
from ..models.role_model import Role
from ..serializers.permission_serializer import *

class RoleCreateSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Role
        exclude = [
            "id",
            "admin"
        ]

    def validate_name(self, attr):
        request = self.context.get("request")

        if Role.objects.filter(
            name=attr,
            admin=request.user.admin,
        ).exists():
            raise serializers.ValidationError(
                "Role with this name already exist."
            )
        
        return attr

class RoleUpdateSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Role
        exclude = [
            "id",
            "admin"
        ]

class RoleListSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "permissions"
        ]

    def get_permissions(self, obj):
        permissions = obj.permissions.all()

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



class RoleRetrieveSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "permissions"
        ]

    def get_permissions(self, obj):
        permissions = obj.permissions.all()

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

class RoleMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        exclude = [
            "permissions",
            "admin",
        ]