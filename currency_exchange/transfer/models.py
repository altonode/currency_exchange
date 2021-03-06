import uuid as uuid_lib

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify

User = get_user_model()

class Transaction(models.Model):
    """Transaction data for money transferred"""
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=765)
    # Distinguish between deposit and money transfer
    is_deposit = models.BooleanField(default=False)
    # transaction unique identifier
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)

    # Return the transaction id
    def __str__(self):
        return self.uuid


class SentMoney(models.Model):
    """ Sender transaction details"""
    date = models.DateTimeField(auto_now=True)
    sender_uuid = models.CharField(blank=False, editable=False, max_length=40)
    transfer_to = models.ForeignKey(User, blank=False, max_length=255, on_delete=models.CASCADE)
    line_amount = models.DecimalField(decimal_places=9, max_digits=20)
    currency = models.CharField(max_length=128)
    rate = models.DecimalField(decimal_places=9, max_digits=20)
    debit = models.DecimalField(default=0, decimal_places=9, max_digits=20)
    credit = models.DecimalField(default=0, decimal_places=9, max_digits=20)
    transaction_uuid = models.OneToOneField(Transaction, on_delete=models.CASCADE)

    # Return the transfer details
    def __str__(self):
        return self.line_amount


class ReceivedMoney(models.Model):
    """ Receiver transaction details"""
    date = models.DateTimeField(auto_now=True)
    receiver_uuid = models.CharField(blank=False, editable=False, max_length=40)
    transfer_from = models.ForeignKey(User, blank=False, max_length=255, on_delete=models.CASCADE)
    line_amount = models.DecimalField(decimal_places=9, max_digits=20)
    currency = models.CharField(blank=False, max_length=128)
    rate = models.DecimalField(decimal_places=9, max_digits=20)
    debit = models.DecimalField(default=0, decimal_places=9, max_digits=20)
    credit = models.DecimalField(default=0, decimal_places=9, max_digits=20)
    transaction_uuid = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    # Return the transfer details
    def __str__(self):
        return self.line_amount


class Account(models.Model):
    """ Wallet User Accounts"""
    # Links Account to a User model instance.
    username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    balance = models.DecimalField(decimal_places=4, max_digits=20, default=0)

    # account unique identifier
    account_number = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)

    # Return account balance
    def __str__(self):
        return self.account_number
