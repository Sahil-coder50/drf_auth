from django.db import models

from django.conf import settings

class Providers(models.TextChoices):
    GOOGLE = ("Google", "google")
    GITHUB = ("Github", "github")

class SocialAccount(models.Model):
    user_id = models.IntegerField(blank=False, null=False)

    provider = models.CharField(
        max_length=20,
        choices=Providers,
    )

    provider_user_id = models.CharField(
        max_length=255
    )

    class Meta:
        unique_together = ("provider", "provider_user_id")
