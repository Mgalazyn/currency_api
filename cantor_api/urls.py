from django.urls import path
from .views import CurrencyDataView, ExchangeRateView, LoadInitialDataView

urlpatterns = [
    path('currency/', CurrencyDataView.as_view(), name='currency-list'),
    path('currency/<str:from_currency>/<str:to_currency>/', ExchangeRateView.as_view(), name='exchange-rate'),
    path('load-initial-data/', LoadInitialDataView.as_view(), name='load-initial-data'),
]