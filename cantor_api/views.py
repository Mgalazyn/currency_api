from django.shortcuts import render
from rest_framework import viewsets
from .models import Currency
import requests
from django.conf import settings

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()

