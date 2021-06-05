from django.db import models
from django.urls import reverse
from django.db.models import constraints

# Create your models here.

class Client(models.Model):
    designation = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    firstName = models.CharField(max_length=120)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)
    email = models.EmailField()

    def __str__(self):
        return (self.firstName + " " + self.name + ", " + self.street + ", " + self.postal_code + " "  + self.city)

    class Meta:
        constraints = [
            constraints.UniqueConstraint(fields=['name', 'firstName', 'street', 'city'], name='unique_client')
        ]

    #def get_absolute_url (self):
        #return reverse("client_list")
