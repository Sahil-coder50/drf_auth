from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from urllib.parse import urlencode

from ..serializers.auth_serializer import LoginSerializer, RegisterSerializer, GoogleSerializer
from ..services.auth_service import AuthService
from ..services.token_service import TokenService
from ..services.jwt_service import JWTService

class AuthViewSet(GenericViewSet):

    @action(detail=False, methods=["POST"])
    def register(self, request):
        
        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = AuthService.register(
            data=serializer.validated_data
        )

        return Response(
            {
                "success": "Registration Successful",
                "detail": {
                    "user": user.email
                }
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["POST"])
    def login(self, request):
        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        data = AuthService.login(
            data=serializer.validated_data
        )

        user = data.pop("user")

        serializer = LoginSerializer(
            data,
            context={"user": user}
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["POST"])
    def logout(self, request):
        refresh_token = request.data.get("refresh")

        if refresh_token:
            token = JWTService.decode_refresh_token(refresh_token)
            TokenService.revoke_family(token["family"])


        return Response(
            {"success": "Logged Out Successfully."},
            status=status.HTTP_205_RESET_CONTENT
        )

    @action(detail=False, methods=["POST"])
    def token_refresh(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh Token Missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        data = TokenService.refresh(refresh_token)

        return Response(
            data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=["GET"], url_path="google/login", url_name="google-login")
    def google(self, request):
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }

        url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            + urlencode(params)
        )

        return Response({"url": url}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="google/callback", url_name="google-callback")
    def callback(self, request):
        serializer = GoogleSerializer(
            data=request.query_params
        )

        serializer.is_valid(raise_exception=True)

        data = AuthService.google_login(
            code=serializer.validated_data["code"]
        )

        user = data.pop("user")

        serializer = LoginSerializer(
            data,
            context={"user": user}
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )