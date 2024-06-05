from django.db import models
from usermanagement.models import User

# Create your models here.
class RoomType(models.Model):
    name = models.CharField(max_length=200)
    amenities = models.CharField(max_length=200)
    
class Room(models.Model):
    room_number = models.IntegerField()
    description = models.TextField()
    type = models.ForeignKey(RoomType,on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=200)
    price = models.FloatField()
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    is_active = models.BooleanField(default=True)

class Invoice(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    total_amount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)