from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.urls import reverse

from currency_exchange.users.models import UserProfile
from currency_exchange.converter.models import Currency
from .transfer import TransferMixin
from . models import Account
from . forms import AccountUpdateForm


User = get_user_model()


class WalletView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/wallet.html'

    def get_context_data(self, username, **kwargs):
        # Create proxy object for the template context
        user = User.objects.get(username=username)
        userprofile = UserProfile.objects.get(username=user)
        preferred_currency = userprofile.preferred_currency
        currency = Currency.objects.get(currency_name=preferred_currency)
        account = Account.objects.get_or_create(username=userprofile.username)[0]
        kwargs['currency'] = currency
        kwargs['userprofile'] = userprofile
        kwargs['account'] = account
        return kwargs


wallet_view = WalletView.as_view()


class AccountUpdateView(LoginRequiredMixin, SuccessMessageMixin, TransferMixin, TemplateView, FormView):

    model = Account
    form_class = AccountUpdateForm
    template_name = 'transfer/accountupdate_form.html'
    success_message = _("Information successfully updated")

    def get_context_data(self, username, **kwargs):
        # Create proxy object for the template context
        user = User.objects.get(username=username)
        userprofile = UserProfile.objects.get(username=user)
        preferred_currency = userprofile.preferred_currency
        currency = Currency.objects.get(currency_name=preferred_currency)
        account = Account.objects.get(username=userprofile.username)
        kwargs['username'] = username
        kwargs['currency'] = currency
        kwargs['userprofile'] = userprofile
        kwargs['account'] = account
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs

    def get_success_url(self):
        return reverse('transfer:wallet', kwargs={'username': self.request.user.username})

    def form_invalid(self, username, form):
        return self.render_to_response(self.get_context_data(username, form=form))

    def form_valid(self, username, form):
        return self.render_to_response(self.get_context_data(username, form=form))

    def post(self, request, *args, **kwargs):
        username = kwargs['username']
        form = self.get_form()
        if form.is_valid():
            deposit = form.cleaned_data['deposit']
            print(deposit)
            print(type(deposit))
            return HttpResponseRedirect('/transfer/~wallet/{}/'.format(username))
        else:
            return self.form_invalid(username, form)


account_update_view = AccountUpdateView.as_view()
