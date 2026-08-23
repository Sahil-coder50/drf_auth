from django.db import models
from django.contrib.auth.models import Permission

class RoleMixin(models.Model):

    roles = models.ForeignKey(
        "auth_drf.Role",
        verbose_name=("roles"),
        on_delete=models.SET_NULL,
        blank=True, null=True,
        help_text=(
            "The role this user belongs to. A user will get all permissions granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("user permissions"),
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, "user")
    
    def get_role_permissions(self, obj=None):
        return _user_get_permissions(self, "role")
    
    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, "all")
    

def _user_get_permissions(user, from_name):
    permissions = set()
    if from_name == "user":
        permissions.update(user.user_permissions.all())
    elif from_name == "role":
        permissions.update(user.roles.permissions.all())
    elif from_name == "all":
        permissions.update(user.user_permissions.all())
        if user.roles is not None:# new con
               permissions.update(user.roles.permissions.all())
    return permissions


#Bas if user.roles is not None: check add kiya — pehle roles=None hone par crash ho raha tha, ab safe fallback ho jayega (empty permissions milenge, crash nahi hoga).

