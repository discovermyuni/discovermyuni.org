import contextlib

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"
    app_name = "users"

    def ready(self):
        with contextlib.suppress(ImportError):
            import discoverutm.users.signals  # noqa: F401
