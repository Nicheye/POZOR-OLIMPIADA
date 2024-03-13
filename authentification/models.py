from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
	username = models.CharField(max_length=255,unique=True)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	name = models.CharField(max_length=20,default='name')
	last_name = models.CharField(max_length=20,default='last_name')
	age = models.PositiveIntegerField(default=18)
	isPublic = models.BooleanField(default=True)
	last_friend_added_at = models.DateTimeField(blank=True, null=True)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

class Friend_Link(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_creator')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_receiver')
    created_at = models.DateField(auto_now_add=True)
