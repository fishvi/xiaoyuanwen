from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "xiaoyuanwen.users"
    verbose_name = "用户"

    def ready(self):
        try:
            import xiaoyuanwen.users.signals  # noqa F401
        except ImportError:
            pass
