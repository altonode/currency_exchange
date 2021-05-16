from django import forms
from django.contrib import admin

from currency_exchange.transfer.models import Account


class WalletForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['username', 'balance', ]


@admin.register(Account)
class WalletForm(admin.ModelAdmin):
    form = WalletForm
    fields = ['username', 'balance', ]
    list_display = ['username', 'account_number', 'balance', ]
    search_fields = ["username"]
