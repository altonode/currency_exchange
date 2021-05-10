import os
import requests
from requests.exceptions import HTTPError


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings.local')

import django
from django.conf import settings
from config.settings import local

settings.configure(default_settings=local, DEBUG=True)
django.setup()

from currency_exchange.converter.models import Currency


def populate():
    # creates a lists of dictionaries containing the available codes from the API
    # Then creates a list of dictionaries with the received codes
    # This allows us to iterate and add the data to converter app models
    url = 'https://v6.exchangerate-api.com/v6/90104cb2e5fc2e3261afaa55/codes'

    try:
        response = requests.get(url)

        # A successful response will raise no error
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = response.json()
        supported = []
        for item in data['supported_codes']:
            supported.append({'code': item[0], 'name': item[1]})
        print(supported)
        print(data)
        for raw_data in supported:
            current = add_currency(raw_data["code"], raw_data["name"])


def add_currency(code, name):
    c = Currency.objects.get_or_create(currency_code=code)[0]
    c.currency_code = code
    c.currency_name = name
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print("Starting converter app population script...")
    populate()
