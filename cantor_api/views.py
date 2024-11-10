from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Currency, ExchangeRate
import requests
import os

class CurrencyDataView(APIView):
    def get(self, request):
        currencies = Currency.objects.all()
        response_data = [{"code": currency.code} for currency in currencies]
        return Response(response_data)

class ExchangeRateView(APIView):
    def get(self, request, from_currency, to_currency):
        # Fetch exchange rate from local database
        try:
            from_currency_obj = Currency.objects.get(code=from_currency)
            to_currency_obj = Currency.objects.get(code=to_currency)
            exchange_rate = ExchangeRate.objects.get(currency_from=from_currency_obj, currency_to=to_currency_obj)
            response_data = {
                "currency_pair": f"{from_currency}{to_currency}",
                "exchange_rate": exchange_rate.rate,
            }
            return Response(response_data)
        except (Currency.DoesNotExist, ExchangeRate.DoesNotExist):
            return Response({"error": "Currency pair not found"}, status=404)

class LoadInitialDataView(APIView):
    def get(self, request):
        api_key = os.getenv('api_key')
        currency_url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"
        
        # Fetch supported currencies codes from the API
        currency_request = requests.get(currency_url)
        currency_response = currency_request.json()
        
        # Load currencies codes into the database
        supported_codes = currency_response.get('supported_codes', [])
        
        for code in supported_codes:
            Currency.objects.get_or_create(code=code[0], name=code[1])

        #pairs for which exchange rate will be avaliable
        initial_pairs = [
            ("EUR", "USD"),
            ("USD", "EUR"),
            ("USD", "JPY"),
            ("JPY", "USD"),
            ("PLN", "USD"),
            ("USD", "PLN"),
        ]
        

        #load exchange rate for listed initial pairs
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

        return Response({"message": "Data loaded successfully."})