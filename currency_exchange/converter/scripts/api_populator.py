import requests
from requests.exceptions import HTTPError

from django.conf import settings

from currency_exchange.converter.models import Currency, ConversionRate


def run(*args):
    # creates a lists of dictionaries containing the available codes from the API
    # Then creates a list of dictionaries with the received codes
    # This allows us to iterate and add the data to converter app models
    api_key = settings.OPEN_EXCHANGE_RATES_APP_ID

    symbols_url = 'https://openexchangerates.org/api/currencies.json'

    rates_url = 'https://openexchangerates.org/api/latest.json?app_id={}'.format(api_key)

    try:
        response1 = requests.get(symbols_url)

        # A successful response will raise no error
        response1.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        symbols_response = response1.json()


    try:
        response2 = requests.get(rates_url)

        # A successful response will raise no error
        response2.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        rates_response = response2.json()

    for symbol, name in symbols_response.items():
        c = add_currency(currency_name=name, currency_symbol=symbol)

    currencies = len(Currency.objects.all())
    print(f'{currencies} world currencies available')

    base_currency = rates_response['base']
    print(f'Base currency is {base_currency}')

    for symbol, rate in rates_response['rates'].items():
        c = Currency.objects.get(currency_symbol=symbol)
        r = add_rate(currency=c, rate=rate)

    rates_count = len(ConversionRate.objects.all())
    print(f'{rates_count} supported codes available')


def add_rate(currency, rate):
    print(f'{currency} conversion rate: {rate}')
    r = ConversionRate.objects.get_or_create(symbol=currency)[0]
    r.rate = rate
    r.save()

    return r


def add_currency(currency_name, currency_symbol):
    print(f'{currency_symbol} >-< {currency_name}')
    c = Currency.objects.get_or_create(currency_symbol=currency_symbol)[0]
    c.currency_name = currency_name
    c.save()
    return c
