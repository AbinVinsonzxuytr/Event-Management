from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Event(models.Model):
    title=models.CharField(max_length=30)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    amount=models.IntegerField()
    venue=models.CharField(max_length=30)
    organizer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    total_seats=models.IntegerField()
    available_seats=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
