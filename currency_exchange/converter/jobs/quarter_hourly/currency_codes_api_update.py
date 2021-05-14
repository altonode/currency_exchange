import requests
from requests.exceptions import HTTPError

from django_extensions.management.jobs import QuarterHourlyJob

urrency


class Job(QuarterHourlyJob):

    response = requests.get(url)

    # A successful response will raise no error
    response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = response.json()

    for i, j in data.items():
        currency_dict = data[i]
        currency_code = currency_dict["currency_code"]
        currency_name = currency_dict["name"]
        country_name = currency_dict["country_name"]
        currency = add_currency(currency_code, currency_name, country_name)

def add_currency(currency_code, currency_name, country_name):
    print(f'{country_name} uses {currency_code} for  the {currency_name}')
    c = Currency.objects.get_or_create(currency_code=currency_code)[0]
    c.currency_code = currency_code
    c.currency_name = currency_name
    c.country_name = country_name
    c.save()
    return c

code_count = len(Currency.objects.all())

print(f'{code_count} supported codes retrieved')
