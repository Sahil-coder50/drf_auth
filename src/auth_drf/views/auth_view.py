from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from ..serializers.auth_serializer import LoginSerializer, RegisterSerializer
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
            serializer.validated_data
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
            serializer.validated_data
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
