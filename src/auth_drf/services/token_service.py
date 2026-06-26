import uuid

from django.utils import timezone

from ..models.token_model import TokenRefresh
from ..services.jwt_service import JWTService

from rest_framework.exceptions import AuthenticationFailed

class TokenService:

    @classmethod
    def issue_token_pair(cls, user):
        family_id = uuid.uuid4()
        jti = uuid.uuid4()

        access_token = JWTService.create_access_token(user)

        refresh_token = JWTService.create_refresh_token(
            user=user,
            jti=jti,
            family_id=family_id,
        )

        TokenRefresh.objects.create(
            user=user,
            jti=jti,
            family_id=family_id,
            expires_at=timezone.now() + timezone.timedelta(days=30),
        )

        return {
            "access": access_token,
            "refresh": refresh_token
        }
    
    @classmethod
    def revoke_family(cls, family_id):
        TokenRefresh.objects.filter(
            family_id=family_id,
            is_revoked=False,
        ).update(
            is_revoked=True,
            revoked_at=timezone.now(),
        )

    @classmethod
    def _detect_reuse(cls, token_obj):
        if token_obj.is_used:
            cls.revoke_family(
                token_obj.family_id
            )

            raise AuthenticationFailed(
                "Refresh token reuse detected."
            )
        
    @classmethod
    def refresh(cls, refresh_token):
        """
        refresh_payload

        {
            "jti": "...",
            "family": "...",
            "sub": "..."
        }

        """
        refresh_payload = JWTService.decode_refresh_token(
            refresh_token
        )

        token_obj = TokenRefresh.objects.get(
            jti=refresh_payload["jti"]
        )

        if token_obj.is_revoked:
            raise AuthenticationFailed(
                "Token revoked."
            )
        if token_obj.expires_at < timezone.now():
            raise AuthenticationFailed(
                "Token Expired."
            )
        cls._detect_reuse(token_obj)

        token_obj.used_at = timezone.now()
        token_obj.is_used = True
        token_obj.save(
            update_fields=["used_at", "is_used"]
        )

        new_jti = uuid.uuid4()

        TokenRefresh.objects.create(
            user=token_obj.user,
            jti=new_jti,
            family_id=token_obj.family_id,
            parent_jti=token_obj.jti,
            expires_at=timezone.now() + timezone.now(days=30),
        )

        access_token = JWTService.create_access_token(token_obj.user)

        refresh_token = JWTService.create_refresh_token(
            user=token_obj.user,
            jti=new_jti,
            family_id=token_obj.family_id,
            parent_jti=token_obj.jti,
        )

        return {
            "access": access_token,
            "refresh": refresh_token,
        }

