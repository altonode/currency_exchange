from django import forms
from django.contrib import admin

from currency_exchange.transfer.models import Account, Transaction, SentMoney, ReceivedMoney


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


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['note', 'is_deposit', ]


@admin.register(Transaction)
class TransactionForm(admin.ModelAdmin):
    form = TransactionForm
    fields = ['note', 'is_deposit', 'transaction_id']
    list_display = ['created', 'modified', 'note', 'is_deposit', 'uuid', ]
    search_fields = ['transaction_id', 'note']


class SenderForm(forms.ModelForm):

    class Meta:
        model = SentMoney
        fields = ['line_amount', 'currency', 'rate', 'debit', 'credit', 'transaction_uuid', ]


@admin.register(SentMoney)
class SenderForm(admin.ModelAdmin):
    form = SenderForm
    fields = ['sender_uuid', 'line_amount', 'currency', 'rate', 'debit', 'credit', 'sent_amount', 'transaction_uuid']
    list_display = ['date', 'sender_uuid', 'transfer_to', 'line_amount', 'currency', 'rate', 'debit', 'credit',
                    'transaction_uuid', ]
    search_fields = ['transfer_to', 'sender_uuid', 'transaction_uuid']


class ReceiverForm(forms.ModelForm):

    class Meta:
        model = ReceivedMoney
        fields = ['line_amount', 'currency', 'rate', 'debit', 'credit', 'transaction_uuid', ]


@admin.register(ReceivedMoney)
class ReceiverForm(admin.ModelAdmin):
    form = ReceiverForm
    fields = ['receiver_uuid', 'transfer_from', 'line_amount', 'currency', 'rate', 'debit', 'credit', 'transaction_uuid']
    list_display = ['date', 'receiver_uuid', 'transfer_from', 'line_amount', 'currency', 'rate', 'debit', 'credit', 'transaction_uuid']
    search_fields = ['transfer_from', 'receiver_uuid', 'transaction_uuid']

