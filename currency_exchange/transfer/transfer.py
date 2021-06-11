from django.contrib.auth import get_user_model

from currency_exchange.converter.models import Currency, ConversionRate
from . models import Account, SentMoney, ReceivedMoney, Transaction


User = get_user_model()


def account_deposit(username, deposit):
    # All deposits done using the Base Currency
    sender_currency = Currency.objects.get(currency_name='United States Dollar')
    sender_rate_obj = ConversionRate.objects.get(symbol=sender_currency)
    sender_rate = sender_rate_obj.rate
    sender_symbol = sender_currency.currency_symbol

    # Admin ledger account user for deposits
    sender_profile = UserProfile.objects.get(uuid='e39d1c8b-3c9f-44e1-a027-e0bc4acea676')

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
    balance = balance + deposit
    print(balance)
    account.balance = balance
    print(balance)
    account.save()

    note = 'DEPOSIT: {} {} deposited to {} wallet account'.format(sent_amount, sender_symbol, username)

    transaction = Transaction.objects.create(note=note, is_deposit=True)
    print(transaction.note)
    transaction.save()

    ReceivedMoney.objects.create(receiver_uuid=receiver_uuid,
                                 transfer_from=sender_profile,
                                 line_amount=sent_amount,
                                 currency=receiver_currency.currency_name,
                                 rate=receiver_rate,
                                 debit=deposit,
                                 transaction_uuid=transaction)


def money_transfer(context, receiverprofile):
    # Sender User Information
    account_uuid = context['account_uuid']
    sender_uuid = context['sender_uuid']
    senderprofile = User.objects.get(uuid=sender_uuid)
    # Get the sender currency symbol
    sender_currency = context['sender_currency']
    # Get the sender line amount
    sent_amount = context['sent_amount']
    sender_rate = context['sender_rate']
    line_amount = sent_amount/sender_rate

    # Receiver User Information
    userprofile = receiverprofile
    preferred_currency = userprofile.preferred_currency
    received_currency = Currency.objects.get(currency_name=preferred_currency)
    receiver_currency = received_currency.currency_name
    receiver_symbol = ConversionRate.objects.get(symbol=received_currency)
    receiver_rate = receiver_symbol.rate
    receiver_uuid = userprofile.uuid

    # Sender account balance before transfer
    sender_account = Account.objects.get(account_number=account_uuid)
    sender_balance = sender_account.balance
    print(sender_balance)
    sender_account.balance = sender_balance - sent_amount
    print(sender_balance)
    sender_account.save()

    # Receiver account information
    receiver = User.objects.get(username=receiverprofile)
    receiver_account = Account.objects.get(username=receiver)
    receiver_balance = receiver_account.balance
    account_number = receiver_account.account_number

    # Convert sent amount to receiver currency
    exchange_rate = sender_rate/receiver_rate
    # Deposit in base currency
    receiver_debit = sent_amount * exchange_rate
    receiver_balance = receiver_balance + sent_amount
    receiver_account.balance = receiver_balance
    receiver_account.save()

    note = 'TRANSFER: {} {} sent by {} from account number {} to {} of account number {} at exchange rate {}: {}->{}'\
        .format(sent_amount, sender_currency, senderprofile, account_uuid, receiverprofile, account_number,
                exchange_rate, sender_currency, receiver_symbol)

    transaction = Transaction.objects.create(note=note)
    print(transaction.note)
    transaction.save()

    SentMoney.objects.create(sender_uuid=sender_uuid,
                             transfer_to=receiverprofile,
                             line_amount=line_amount,
                             currency=sender_currency,
                             rate=sender_rate,
                             credit=sent_amount,
                             transaction_uuid=transaction)

    ReceivedMoney.objects.create(receiver_uuid=receiver_uuid,
                                 transfer_from=senderprofile,
                                 line_amount=line_amount,
                                 currency=receiver_currency,
                                 rate=receiver_rate,
                                 debit=receiver_debit,
                                 transaction_uuid=transaction)
