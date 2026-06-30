from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings

from rest_framework.exceptions import ValidationError

from ..services.token_service import TokenService
from ..services.role_service import RoleService
from ..services.permissions_service import PermissionService
from ..models.role_model import Role
from ..models.oauth_model import SocialAccount, Providers

import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

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
            email_or_username=data["email_or_username"],
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
    
    @classmethod
    def google_login(cls, *, code):
        TOKEN_URL = "https://oauth2.googleapis.com/token"

        response = requests.post(
            TOKEN_URL,
            data={
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            },
            timeout=10,
        )

        response.raise_for_status()

        tokens = response.json()

        info = id_token.verify_oauth2_token(
            tokens["id_token"],
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )

        user = User.objects.filter(
            email=info.get("email"),
        )
        if user.exists() and SocialAccount.objects.filter(
            user_id=user.first().id,
            provider=Providers.GOOGLE,
            provider_user_id=info.get("sub")
        ):
            user = user.first()

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
        else:
            user = User.objects.create(
                email=info.get("email"),
                username=info.get("username", info.get("email")),
                email_or_username=info.get("email"),
                first_name=info.get("given_name"),
                last_name=info.get("family_name"),
            )
            social = SocialAccount.objects.create(
                provider=Providers.GOOGLE,
                provider_user_id=info.get("sub"),
                user_id=user.id
            )

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






