from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from currency_exchange.users.models import UserProfile
from currency_exchange.converter.models import Currency

User = get_user_model()


class WalletView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/wallet.html'

    def get_context_data(self, username, **kwargs):
        # Create proxy object for the template context
        user = User.objects.get(username=username)
        userprofile = UserProfile.objects.get(username=user)
        preferred_currency = userprofile.preferred_currency
        currency = Currency.objects.get(currency_name=preferred_currency)
        kwargs['currency'] = currency
        kwargs['userprofile'] = userprofile
        return kwargs


wallet_view = WalletView.as_view()
