from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TransferConfig(AppConfig):
    name = "currency_exchange.transfer"
    verbose_name = _("Transfer")

    def ready(self):
        try:
            import currency_exchange.transfer.signals  # noqa F401
        except ImportError:
            pass
