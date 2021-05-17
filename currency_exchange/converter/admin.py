from django import forms
from django.contrib import admin
from currency_exchange.converter.models import Currency, ConversionRate


class CurrencyForm(forms.ModelForm):

    class Meta:
        model = Currency
        fields = ['currency_symbol', 'currency_name', ]


@admin.register(Currency)
class CurrencyForm(admin.ModelAdmin):
    form = CurrencyForm
    fields = ['currency_symbol', 'currency_name', ]
    list_display = ["currency_symbol", "currency_name",]
    search_fields = ["currency_symbol"]

class ConversionForm(forms.ModelForm):

    class Meta:
        model = ConversionRate
        fields = ['rate', 'symbol', ]


@admin.register(ConversionRate)
class CurrencyForm(admin.ModelAdmin):
    form = ConversionForm
    fields = ['rate', 'symbol', ]
    list_display = ["symbol", "rate",]
    search_fields = ["symbol"]
