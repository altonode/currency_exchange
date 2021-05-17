from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse

from currency_exchange.users.models import UserProfile
from currency_exchange.converter.models import Currency, ConversionRate
from .models import Account, SentMoney, ReceivedMoney, Transaction

User = get_user_model()


class TransferMixin(object):

    def render_transfer_response(self, kwargs, **response_kwargs):
        form = kwargs['form']
        user_profile = kwargs['userprofile']
        account = Account.objects.get(username=user_profile.username)
        balance = account.balance
        deposit = form['balance'].value()
        balance += deposit
        print(type(balance))
        print(balance)
        currency = kwargs['currency']

        # All deposits done using the Base Currency
        sender_currency = Currency.objects.get(currency_name='United States Dollar')
        sender_rate_obj = ConversionRate.objects.get(symbol=sender_currency)
        # Admin ledger account user for deposits
        sender_profile = UserProfile.objects.get(uuid='88069a9b-1a84-416f-9b4c-6e310f5ec886')

        receiver_symbol = ConversionRate.objects.get(symbol=currency)
        receiver_rate = receiver_symbol.rate
        receiver_uuid = user_profile.uuid

        sender_rate = sender_rate_obj.rate
        sender_symbol = sender_currency.currency_symbol

        # Convert deposited amount to base currency (USD)
        exchange_rate = sender_rate/receiver_rate

        rate = Decimal(exchange_rate)
        print(type(rate))
        print(rate)
        sent_amount = deposit * rate

        note = '{} {} deposited to {} wallet account'.format(sent_amount, sender_rate, User.username)

        transaction = Transaction.objects.create(note=note, is_deposit=True)
        transaction.save()

        received_money = ReceivedMoney.objects.create(receiver_uuid=receiver_uuid,
                                                      transfer_from=sender_profile,
                                                      line_amount=sent_amount,
                                                      currency=currency.currency_name,
                                                      rate=receiver_rate,
                                                      debit=deposit,)
        return reverse('transfer:wallet',
                       kwargs={'username': self.request.user.username})

