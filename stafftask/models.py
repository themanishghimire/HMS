from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class Staff(models.Model):
    staff_name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    shift = models.CharField(max_length=100)

class Task(models.Model):
    description = models.TextField()
    assigned_to = models.ForeignKey(Staff, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    deadline = models.DateField()
