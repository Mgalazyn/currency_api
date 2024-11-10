from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cantor_api.models import Currency, ExchangeRate


class CurrencyExchangeAPITests(APITestCase):
    def setUp(self):
        # Set up initial data for tests
        self.currency_eur = Currency.objects.create(code='EUR', name='Euro')
        self.currency_usd = Currency.objects.create(code='USD', name='United States Dollar')
        self.exchange_rate = ExchangeRate.objects.create(
            currency_from=self.currency_eur,
            currency_to=self.currency_usd,
            rate=1.2000
        )

    def test_currency_data_view(self):
        """Test the CurrencyDataView endpoint"""
        url = reverse('currency-list') 
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn({'code': 'EUR'}, response.data)
        self.assertIn({'code': 'USD'}, response.data)
        print("TEST1 - passed")

    def test_exchange_rate_view(self):
        """Test the ExchangeRateView endpoint"""
        url = reverse('exchange-rate', args=['EUR', 'USD'])  
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['currency_pair'], 'EURUSD')
        self.assertAlmostEqual(float(response.data['exchange_rate']), float(self.exchange_rate.rate), places=4)
        print("TEST2 - passed")

    def test_exchange_rate_view_not_found(self):
        """Test the ExchangeRateView for a non-existing currency pair"""
        url = reverse('exchange-rate', args=['EUR', 'JPY'])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Currency pair not found"})
        print("TEST3 - passed")

    def test_load_initial_data_view(self):
        """Test the LoadInitialDataView endpoint"""
        url = reverse('load-initial-data')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Data loaded successfully."})
        self.assertTrue(Currency.objects.count() > 0)
        print("TEST4 - passed")
