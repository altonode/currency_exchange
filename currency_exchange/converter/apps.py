from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "currency_exchange.converter"
    verbose_name = _("Converter")

    def ready(self):
        try:
            import currency_exchange.converter.signals  # noqa F401
        except ImportError:
            pass
