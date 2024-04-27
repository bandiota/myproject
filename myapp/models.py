from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    modified_on = models.DateTimeField(auto_now=True)
    fullname = models.CharField(max_length=100)
    designation = models.CharField(max_length=40, null=True, blank=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, null=True)
    address = models.TextField(null=True)
    profile_picture = models.ImageField(upload_to='images/')
    is_super = models.BooleanField(default=False)

    def __str__ (self):
        return self.fullname


class Notification(models.Model):
    message = models.TextField()
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    is_read = models.BooleanField(default=False)

    def __str__ (self):
        return self.receiver.fullname
