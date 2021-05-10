from django import forms
from django.contrib import admin
from currency_exchange.converter.models import Currency


class CurrencyForm(forms.ModelForm):

    class Meta:
        model = Currency
        fields = ['currency_code', 'currency_name']


@admin.register(Currency)
class CurrencyForm(admin.ModelAdmin):
    form = CurrencyForm
    fields = ['currency_code', 'currency_name']
