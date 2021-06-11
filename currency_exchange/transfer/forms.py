from django import forms
from django.contrib.auth import get_user_model

from .models import SentMoney


User = get_user_model()


class AccountUpdateForm(forms.Form):

    deposit = forms.DecimalField(required=True, decimal_places=9, max_digits=20)


class SentMoneyForm(forms.ModelForm):
    query_set = User.objects.all()
    transfer_to = forms.ModelChoiceField(queryset=query_set, empty_label="Person to receive money")
    credit = forms.DecimalField(required=True, decimal_places=9, max_digits=20)

    class Meta:

        model = SentMoney
        fields = ('transfer_to', 'credit', )
