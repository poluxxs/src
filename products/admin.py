from django.contrib import admin

from .models import Product_tmp
from .models import Product
# Register your models here.

admin.site.register(Product)
admin.site.register(Product_tmp)
