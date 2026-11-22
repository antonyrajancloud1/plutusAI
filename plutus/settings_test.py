# Test-only settings: in-memory SQLite so tests never touch the live MySQL DB.
from plutus.settings import *  # noqa: F401,F403

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CELERY_TASK_ALWAYS_EAGER = True
# Fast hashing: the default PBKDF2 makes every test user take ~1s to create.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
