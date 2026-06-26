from django.db import models
from django.contrib.auth.models import Permission

from django.conf import settings

class Role(models.Model):
    
    name = models.CharField(max_length=150)

    permissions = models.ManyToManyField(
        Permission,
        verbose_name=("role permissions"),
        help_text="Role Based Permissions",
    )

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users",
    )

    class Meta:
        unique_together = ("name", "admin")

