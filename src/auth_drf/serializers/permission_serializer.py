from rest_framework import serializers
from django.contrib.auth.models import Permission

class PermissionSerializer(serializers.Serializer):
    module = serializers.CharField(max_length=255)
    actions = serializers.ListField(
        child=serializers.CharField(max_length=100),
        allow_empty=True
    )
    