from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    """Currency symbols available from the Open Exchange Rates API"""
    currency_symbol = models.CharField(_("Currency Symbol"),  max_length=4)
    currency_name = models.CharField(_("Name of Currency"), max_length=128)

    class Meta:
        verbose_name_plural = 'currencies'
        ordering = ('currency_name',)

    def __str__(self):
        return self.currency_name


class ConversionRate(models.Model):
    """Latest conversion rates from Open Exchange Rates endpoint"""
    currency = models.OneToOneField(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(_("Conversion Rate - USD"), decimal_places=9, max_digits=20)

    class Meta:
        ordering = ('currency',)

    def __str__(self):
        return str(self.currency)

