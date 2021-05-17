from django import forms

from .models import Account


class AccountUpdateForm(forms.Form):

    deposit = forms.DecimalField(required=True, decimal_places=9, max_digits=20)
