SECRET_KEY = "test-secret-key"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "auth_drf",
]
AUTH_USER_MODEL = "auth.User"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
USE_TZ = True
MIGRATION_MODULES = {"auth_drf": None}