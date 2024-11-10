from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"code: {self.code}"
    
class ExchangeRate(models.Model):
    currency_from = models.ForeignKey(Currency, related_name='exchange_from', on_delete=models.CASCADE)
    currency_to = models.ForeignKey(Currency, related_name='exchange_to', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.currency_from.code} to {self.currency_to.code}: {self.rate}"
    
