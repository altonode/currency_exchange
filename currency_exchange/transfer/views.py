from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic import FormView

from currency_exchange.users.models import UserProfile
from currency_exchange.converter.models import Currency, ConversionRate
from . models import Account, ReceivedMoney, SentMoney
from . forms import AccountUpdateForm, SentMoneyForm
from .transfer import account_deposit, money_transfer


User = get_user_model()


class WalletView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/wallet.html'

    def get_context_data(self, username, **kwargs):
        # Create proxy object for the template context
        user = User.objects.get(username=username)
        userprofile = UserProfile.objects.get(username=user)
        preferred_currency = userprofile.preferred_currency
        currency = Currency.objects.get(currency_name=preferred_currency)
        conversion = ConversionRate.objects.get(symbol=currency)
        account = Account.objects.get_or_create(username=userprofile.username)[0]
        balance = account.balance
        rate = conversion.rate
        amount = balance*rate
        user_uuid = userprofile.uuid
        money_sent = SentMoney.objects.filter(sender_uuid=user_uuid)
        money_received = ReceivedMoney.objects.filter(receiver_uuid=user_uuid)
        for money in money_sent:
            print(money.transfer_to)
            print(money.debit)
        for money in money_received:
            print(money.transfer_from)
            print(money.debit)
        kwargs['currency'] = currency
        kwargs['userprofile'] = userprofile
        kwargs['account'] = account
        kwargs['amount'] = amount
        kwargs['money_sent'] = money_sent
        kwargs['money_received'] = money_received
        return kwargs


wallet_view = WalletView.as_view()


class MoneyTransferView(LoginRequiredMixin, TemplateView, FormView):

    model = Account
    form_class = SentMoneyForm
    template_name = 'transfer/moneytransfer_form.html'

    def get_context_data(self, account_uuid, **kwargs):
        # Create proxy object for the template context
        account = Account.objects.get(account_number=account_uuid)
        user = account.username
        userprofile = UserProfile.objects.get(username=user)
        preferred_currency = userprofile.preferred_currency
        currency = Currency.objects.get(currency_name=preferred_currency)
        kwargs['username'] = user.username
        kwargs['currency'] = currency
        kwargs['userprofile'] = userprofile
        kwargs['account'] = account
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs

    def form_invalid(self, account_uuid, form):
        return self.render_to_response(self.get_context_data(account_uuid, form=form))

    def form_valid(self, account_uuid, form):
        return self.render_to_response(self.get_context_data(account_uuid, form=form))

    def post(self, request, *args, **kwargs):
        user = self.request.user
        userprofile = UserProfile.objects.get(username=user)
        sender_uuid = userprofile.uuid
        sender_currency = userprofile.preferred_currency
        currency = Currency.objects.get(currency_name=sender_currency)
        conversion = ConversionRate.objects.get(symbol=currency)
        form = self.get_form()
        account_uuid = kwargs['account_uuid']
        account = Account.objects.get(account_number=account_uuid)
        balance = account.balance
        print(balance)
        if form.is_valid():
            sent_amount = form.cleaned_data['credit']
            if sent_amount > balance:
                raise ValidationError("Insufficient balance")
            receiverprofile = form.cleaned_data['transfer_to']
            context={}
            context['sender_uuid'] = sender_uuid
            context['sender_currency'] = currency.currency_name
            context['sender_rate'] = conversion.rate
            context['sent_amount'] = sent_amount
            context['account_uuid'] = account_uuid
            money_transfer(context, receiverprofile)
            return HttpResponseRedirect('/transfer/~wallet/{}/'.format(user.username))
        else:
            return self.form_invalid(account_uuid, form)


money_transfer_view = MoneyTransferView.as_view()


class AccountUpdateView(LoginRequiredMixin, TemplateView, FormView):

    model = Account
    form_class = AccountUpdateForm
    template_name = 'transfer/accountupdate_form.html'

    def get_context_data(self, username, **kwargs):
        # Create proxy object for the template context
        user = User.objects.get(username=username)
        userprofile = UserProfile.objects.get(username=user)
        preferred_currency = userprofile.preferred_currency
        currency = Currency.objects.get(currency_name=preferred_currency)
        account = Account.objects.get(username=user)
        kwargs['username'] = username
        kwargs['currency'] = currency
        kwargs['userprofile'] = userprofile
        kwargs['account'] = account
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs

    def form_invalid(self, username, form):
        return self.render_to_response(self.get_context_data(username, form=form))

    def form_valid(self, username, form):
        return self.render_to_response(self.get_context_data(username, form=form))

    def post(self, request, *args, **kwargs):
        username = kwargs['username']
        form = self.get_form()
        if form.is_valid():
            deposit = form.cleaned_data['deposit']
            account_deposit(username, deposit)
            return HttpResponseRedirect('/transfer/~wallet/{}/'.format(username))
        else:
            return self.form_invalid(username, form)


account_update_view = AccountUpdateView.as_view()
