from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework.exceptions import ValidationError

from ..services.token_service import TokenService
from ..services.role_service import RoleService
from ..services.permissions_service import PermissionService
from ..models.role_model import Role

User = get_user_model()

class AuthService:

    @classmethod
    @transaction.atomic
    def register(cls, *, data):
        password = data.pop("password")
        
        user = User.objects.create(
            **data
        )
        user.set_password(password)
        user.admin=user
        user.save()

        permissions = PermissionService.list_all()
        permissions_instances = PermissionService.list_all_instances()

        data = {
            "name": "Administrator",
            "permissions": permissions
        }

        role = RoleService.create(
            data=data,
            user=user
        )
        user.roles=role
        user.user_permissions.set(permissions_instances)

        user.save()

        return user

    @classmethod
    def login(cls, *, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if not user:
            raise ValidationError("Invalid credentials")

        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.roles,
            "user": user,
        }

        token = TokenService.issue_token_pair(user)

        user_data.update(token)

        return user_data