from django import forms

from currency_exchange.users.models import UserProfile
from .models import SentMoney


class AccountUpdateForm(forms.Form):

    deposit = forms.DecimalField(required=True, decimal_places=9, max_digits=20)


class SentMoneyForm(forms.ModelForm):
    query_set = UserProfile.objects.all()
    credit = forms.DecimalField(required=True, decimal_places=9, max_digits=20)

    class Meta:

        model = SentMoney
        fields = ('credit', )



