from django.contrib.auth import get_user_model


from currency_exchange.users.models import UserProfile
from currency_exchange.converter.models import Currency, ConversionRate
from . models import Account, ReceivedMoney, Transaction


User = get_user_model()


def account_deposit(username, deposit):
    # All deposits done using the Base Currency
    sender_currency = Currency.objects.get(currency_name='United States Dollar')
    sender_rate_obj = ConversionRate.objects.get(symbol=sender_currency)
    sender_rate = sender_rate_obj.rate
    sender_symbol = sender_currency.currency_symbol
    # Admin ledger account user for deposits
    sender_profile = UserProfile.objects.get(uuid='88069a9b-1a84-416f-9b4c-6e310f5ec886')

    # Receiver User Information
    user = User.objects.get(username=username)
    userprofile = UserProfile.objects.get(username=user)
    preferred_currency = userprofile.preferred_currency
    receiver_currency = Currency.objects.get(currency_name=preferred_currency)
    receiver_symbol = ConversionRate.objects.get(symbol=receiver_currency)
    receiver_rate = receiver_symbol.rate
    receiver_uuid = userprofile.uuid

    # Receiver Account Balance in USD (base currency)
    account = Account.objects.get(username=user)
    balance = account.balance

    # Convert deposited amount to base currency (USD)
    exchange_rate = sender_rate/receiver_rate
    # Deposit in base currency
    sent_amount = deposit * exchange_rate
    balance = balance + sent_amount
    print(balance)
    account.balance = balance
    account.save()


    note = '{} {} deposited to {} wallet account'.format(sent_amount, sender_symbol, username)
    transaction = Transaction.objects.create(note=note, is_deposit=True)
    print(transaction.note)
    transaction.save()

    ReceivedMoney.objects.create(receiver_uuid=receiver_uuid,
                                 transfer_from=sender_profile,
                                 line_amount=sent_amount,
                                 currency=receiver_currency.currency_name,
                                 rate=receiver_rate,
                                 debit=deposit,
                                 transaction_id=transaction
                                 ,)
