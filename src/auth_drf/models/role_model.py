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

    admin_id = models.IntegerField(blank=False, null=False)

    class Meta:
        unique_together = ("name", "admin_id")

