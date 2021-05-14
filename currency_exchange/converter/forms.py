from django import forms

from .models import Currency

query_set = Currency.objects.all()


class ConverterForm(forms.Form):
    """ Form for handling currency conversion """
    currency_from = forms.ModelChoiceField(queryset=query_set, empty_label="Currency to convert from")
    amount_from = forms.DecimalField(required=True, decimal_places=9, max_digits=20)
    currency_to = forms.ModelChoiceField(queryset=query_set, empty_label="Currency to convert to")
