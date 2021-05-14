import uuid as uuid_lib

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify


class Currency(models.Model):
    """Currency symbols available from the Open Exchange Rates API"""
    currency_symbol = models.CharField(_("Currency Symbol"),  max_length=4)
    currency_name = models.CharField(_("Name of Currency"), max_length=128)

    class Meta:
        verbose_name_plural = 'currencies'
        ordering = ('currency_name',)

    def __str__(self):
        return self.currency_symbol


class ConversionRate(models.Model):
    """Latest conversion rates from Open Exchange Rates endpoint"""
    symbol = models.OneToOneField(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(_("Conversion Rate - USD"), decimal_places=9, max_digits=20)


    class Meta:
        ordering = ('symbol',)


    def __str__(self):
        return str(self.symbol)



class Transaction(models.Model):
    """Transaction data for money transferred"""
    created=models.DateTimeField(auto_now=True)
    modified=models.DateTimeField(auto_now_add=True)
    # transaction unique identifier
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)
    # transaction id slug
    transaction_id = models.SlugField(unique=True)

    # update transaction id
    def save(self, *args, **kwargs):
        self.slug = slugify(self.uuid)
        super(Transaction, self).save(*args, **kwargs)

    # Return the transaction id
    def __str__(self):
        return self.transaction_id


class SentMoney(models.Model):
    """ Sender transaction details"""
    date = models.DateTimeField(auto_now=True)
    transfer_to = models.CharField(blank=False, editable=False, max_length=255)
    line_amount = models.DecimalField(decimal_places=2, max_digits=20)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(decimal_places=4, max_digits=20)
    debit = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    sent_amount = models.IntegerField(blank=False)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    # Return the transfer details
    def __str__(self):
        return self.transfer_to


class ReceivedMoney(models.Model):
    """ Receiver transaction details"""
    date = models.DateTimeField(auto_now=True)
    transfer_from = models.CharField(blank=False, editable=False, max_length=255)
    line_amount = models.DecimalField(decimal_places=2, max_digits=20)
    recipient = models.CharField(blank=False, max_length=255)
    currency = models.CharField(blank=False, max_length=128)
    rate = models.DecimalField(decimal_places=4, max_digits=20)
    debit = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    sent_amount = models.IntegerField(blank=False)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    # Return the transfer details
    def __str__(self):
        return self.transfer_from



