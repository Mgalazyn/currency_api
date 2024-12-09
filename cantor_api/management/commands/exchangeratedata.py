from django.core.management.base import BaseCommand, CommandError
import os 
import requests 
from cantor_api.models import Currency, ExchangeRate


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        api_key = os.getenv('api_key')
        
        currency_url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"

        try:
            currency_request = requests.get(currency_url)
            currency_response = currency_request.json()
        except requests.RequestException:
            raise CommandError(f"Error with fetching data: {requests.RequestException}")
        
        supported_codes = currency_response.get('supported_codes', [])

        for code in supported_codes:
            Currency.objects.get_or_create(code=code[0], name=code[1])

        initial_pairs = [
            ("EUR", "USD"),
            ("USD", "EUR"),
            ("USD", "JPY"),
            ("JPY", "USD"),
            ("PLN", "USD"),
            ("USD", "PLN"),
        ]

        for from_code, to_code in initial_pairs:
            exchange_rate_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_code}"

            rate_request = requests.get(exchange_rate_url)
            rate_response = rate_request.json()

            if 'conversion_rates' in rate_response:
                rate_value = rate_response['conversion_rates'].get(to_code)
                if rate_value is not None:
                    from_currency_obj = Currency.objects.get(code=from_code)
                    to_currency_obj = Currency.objects.get(code=to_code)
                    ExchangeRate.objects.get_or_create(currency_from=from_currency_obj,
                                                        currency_to=to_currency_obj,
                                                        rate=rate_value)

