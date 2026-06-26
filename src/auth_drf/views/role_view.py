from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..serializers.role_serializer import *
from ..services.role_service import RoleService

class RoleViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        
        serializer = RoleCreateSerializer(
            data=request.data,
            context={
                "request": request,
            }
        )

        serializer.is_valid(raise_exception=True)

        role = RoleService.create(
            data=serializer.validated_data,
            user=request.user
        )

        serializer = RoleRetrieveSerializer(
            role
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, pk=None):

        role = RoleService.retrieve(
            id=pk
        )
        
        serializer = RoleUpdateSerializer(
            role,
            data=request.data,
            partial=True,
            context={
                "request": request,
            }
        )

        serializer.is_valid(raise_exception=True)

        role = RoleService.update(
            data=serializer.validated_data,
            role=role,
            user=request.user
        )

        serializer = RoleRetrieveSerializer(
            role
        )

        return Response(
            {
                "success": "Role is Updated",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def list(self, request):
        
        roles = RoleService.list(
            request.user
        )

        serializer = RoleListSerializer(
            roles,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):

        role = RoleService.retrieve(
            id=pk
        )

        serializer = RoleRetrieveSerializer(
            role
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
