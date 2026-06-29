from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class Providers(models.TextChoices):
    GOOGLE = ("Google", "google")
    GITHUB = ("Github", "github")

class SocialAccount(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="social_accounts",
    )

    provider = models.CharField(
        max_length=20,
        choices=Providers,
    )

    provider_user_id = models.CharField(
        max_length=255
    )

    class Meta:
        unique_together = ("provider", "provider_user_id")
