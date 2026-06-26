import uuid

from django.conf import settings
from django.db import models


class TokenRefresh(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="refresh_tokens",
    )

    jti = models.UUIDField(
        unique=True,
        db_index=True,
    )

    family_id = models.UUIDField(
        db_index=True,
    )

    parent_jti = models.UUIDField(
        null=True,
        blank=True,
    )

    is_revoked = models.BooleanField(
        default=False,
    )

    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    is_used = models.BooleanField(
        default=False
    )

    used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    compromised = models.BooleanField(
        default=False,
    )

    class Meta:
        indexes = [
            models.Index(fields=["family_id"]),
            models.Index(fields=["user"]),
            models.Index(fields=["expires_at"]),
        ]