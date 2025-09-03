import contextlib

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"
    app_name = "users"

    def ready(self):
        with contextlib.suppress(ImportError):
            from . import signals  # noqa: F401, PLC0415
