from django.contrib.auth.models import Permission

from ..serializers.permission_serializer import PermissionSerializer

class PermissionService:

    @staticmethod
    def list_all():
        permissions = Permission.objects.all()

        grouped_data = {}

        for perm in permissions:
            if perm.content_type.app_label not in grouped_data:
                grouped_data[perm.content_type.app_label] = []
            grouped_data[perm.content_type.app_label].append(perm.codename)
        
        formatted_list = [
            {"module": module, "actions": actions}
            for module, actions in grouped_data.items()
        ]

        return PermissionSerializer(
            formatted_list,
            many=True
        ).data
    
    @staticmethod
    def list_all_instances():
        permissions = list(Permission.objects.all())

        return permissions

