from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q
from django.db.models import constraints
from decimal import Decimal

from transactions.models import Transaction
from decimal import Decimal
# Create your models here.


class Product(models.Model):
    designation = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.0'))])
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    def __str__(self):
        return self.designation


class Product_tmp(models.Model):
    designation = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.0'))])

    def __str__(self):
        return self.designation
