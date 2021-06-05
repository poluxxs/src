from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Q
from django.db.models import constraints
from decimal import Decimal

from clients.models import Client

# Create your models here.

class Transaction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.TextField()
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.0'))])
    delivery_location_1 = models.CharField(max_length=120)
    delivery_location_2 = models.CharField(max_length=120)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    execution_date = models.DateField(auto_now_add=True, auto_now=False)
    class Meta:
        constraints = [
            constraints.CheckConstraint(
                check=Q(delivery_fee__gte=Decimal('0.0')),
                name='delivery_fee_positive'
            )
        ]
    #Transaction.objects.create(clientName = ergegr b, wrtwetg , 2w4t24)
    def __str__(self):
        return str(self.id)
