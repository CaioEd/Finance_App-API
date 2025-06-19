from django.db import models
from django.contrib.auth.models import User


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances', null=True)
    date = models.DateField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    def __str__(self):
        return f"Balance for {self.data.strftime("%B %Y")}"