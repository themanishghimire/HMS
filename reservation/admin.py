from django.contrib import admin
from .models import Room, RoomType, Reservation, Invoice

# Register your models here.
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Reservation)
admin.site.register(Invoice)
