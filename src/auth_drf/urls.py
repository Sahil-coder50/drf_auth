from django.urls import path

from rest_framework import routers

from .views.auth_view import AuthViewSet
from .views.role_view import RoleViewSet

router = routers.DefaultRouter()

router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"roles", RoleViewSet, basename="roles")

urlpatterns = [
] + router.urls