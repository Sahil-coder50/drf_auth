from django.test import TestCase
from django.db import models
from django.contrib.auth.models import Permission
from .models.user_model import BaseUser

class TestUser(BaseUser):
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="test_user_set",
        related_query_name="test_user",
    )

    class Meta:
        app_label = "auth_drf"

class UserModelTests(TestCase):
    def test_get_full_name(self):
        user = TestUser(first_name="Sahil", last_name="Kumar")
        self.assertEqual(user.get_full_name(), "Sahil Kumar")

    def test_get_full_name_strips_extra_space(self):
        user = TestUser(first_name="Sahil", last_name="")
        self.assertEqual(user.get_full_name(), "Sahil")

    def test_get_short_name(self):
        user = TestUser(first_name="Sahil", last_name="Kumar")
        self.assertEqual(user.get_short_name(), "Sahil")

    def test_default_is_active_true(self):
        user = TestUser()
        self.assertTrue(user.is_active)

    def test_default_is_staff_false(self):
        user = TestUser()
        self.assertFalse(user.is_staff)

    def test_role_permissions_when_no_role_assigned(self):
      user = TestUser.objects.create(first_name="Sahil")
      permissions = user.get_all_permissions()
      self.assertEqual(permissions, set())