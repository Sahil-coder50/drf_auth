from ..models.role_model import Role

from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Permission

class RoleService:

    @staticmethod
    def create(*, data, user):
        permissions = data.pop("permissions")

        code_names = [
            action
            for perm in permissions if isinstance(perm, dict)
            for action in perm.get("actions", [])
        ]

        if code_names:
            permission_instance = list(Permission.objects.filter(codename__in=code_names))

        
        role = Role.objects.create(
            **data,
            admin_id=user.admin.id
        )

        role.permissions.set(permission_instance)
        role.save()

        return role

    @staticmethod
    def update(*, data, role, user):

        has_permission_key = "permissions" in data
        permission_list = data.pop("permissions", [])
        
        for key, value in data.items():
            setattr(role, key, value)

        role.save()

        if has_permission_key:
            code_names = [
                action
                for perm in permission_list if isinstance(perm, dict)
                for action in perm.get("actions", [])
            ]

            if code_names:
                permission_instances = list(Permission.objects.filter(codename__in=code_names))

                role.permissions.set(permission_instances)
            else:
                role.permissions.clear()

        return role

    @staticmethod
    def list(user):
        
        roles = Role.objects.filter(
            admin_id=user.admin.id if user.admin else user.id
        ).prefetch_related("permissions")

        return roles

    @staticmethod
    def retrieve(*, id):
        try:
            role = Role.objects.prefetch_related("permissions").get(
                id=id
            )
        except Role.DoesNotExist:
            raise ValidationError({
                "detail": "Role with given query does not exist."
            })
        else:
            return role