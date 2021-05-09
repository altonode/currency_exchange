import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

from currency_exchange.users import models as user_models

class Currency(models.Model):
    """Codes supported by ExchangeRate-API endpoint"""
    currency_code = models.CharField(_("ISO 4217 currency codes"),  blank=False, max_length=3, default='USD')
    currency_name = models.CharField(_("Supported Currencies"), blank=False, max_length=128)

    def __str__(self):
        return self.currency_name


class ConversionRates(models.Model):
    """Latest conversion rates from ExchangeRate-API endpoint"""
    rate = models.DecimalField(blank=False, decimal_places=4)
    name = models.ForeignKey(Currency, on_delete=models.CASCADE)


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
    date=models.DateTimeField(auto_now=True)
    transfer=models.CharField(blank=False, editable=False, max_length=255)
    line_amount=models.DecimalField(decimal_places=2)
    recipient=models.ForeignKey(user_models.User)
    currency=models.ForeignKey(Currency)
    rate=models.DecimalField(decimal_places=4)
    debit=models.IntegerField(default=0)
    credit=models.IntegerField(default=0)
    sent_amount=models.IntegerField(blank=False)
    transaction_id=models.ForeignKey(Transaction)

    # Return the transfer details
    def __str__(self):
        return self.transfer


class ReceivedMoney(models.Model):
    """ Receiver transaction details"""
    date = models.DateTimeField(auto_now=True)
    transfer = models.CharField(blank=False, editable=False, max_length=255)
    line_amount = models.DecimalField(decimal_places=2)
    recipient = models.CharField(blank=False)
    currency = models.CharField(blank=False)
    rate = models.DecimalField(decimal_places=4)
    debit = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    sent_amount = models.IntegerField(blank=False)
    transaction_id = models.ForeignKey(Transaction)

    # Return the transfer details
    def __str__(self):
        return self.transfer

