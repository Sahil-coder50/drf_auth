import uuid

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed

class JWTService:

    @staticmethod
    def create_access_token(user):
        token = AccessToken.for_user(user)

        return str(token)
    
    @staticmethod
    def create_refresh_token(*, user, jti, family_id, parent_jti=None):    
        token = RefreshToken.for_user(user)

        token["jti"] = str(jti)
        token["family"] = str(family_id)
        token["sub"] = str(user.id)

        if parent_jti:
            token["parent"] = str(parent_jti)
 
        return str(token)
    
    @staticmethod
    def decode_refresh_token(token: str) -> dict:
        try:
            refresh = RefreshToken(token)

            return refresh
        except TokenError as exc:
            raise AuthenticationFailed(
                f"Invalid refresh token: {exc}"
            )
