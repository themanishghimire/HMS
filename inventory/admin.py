from django.contrib import admin
from .models import Supplier, InventoryItem

# Register your models here.
admin.site.register(Supplier)
admin.site.register(InventoryItem)
