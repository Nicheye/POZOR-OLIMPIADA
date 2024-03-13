from django.db import models
from authentification.models import User
# Create your models here.
class Country(models.Model):
	name = models.TextField()
	alpha2 = models.TextField(max_length=2)
	alpha3 = models.TextField(max_length=3)
	region = models.TextField()
	def __str__(self) -> str:
		return str(self.name)

class Publication(models.Model):
	title = models.CharField(max_length=205)
	theme = models.CharField(max_length=205)
	text = models.CharField(max_length=205)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE)
	created_at = models.DateField(auto_now_add=True)
	likesCount = models.PositiveIntegerField(default=0)
	dislikesCount = models.PositiveIntegerField(default=0)

class Like(models.Model):
	pub = models.ForeignKey(Publication,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

class DisLike(models.Model):
	pub = models.ForeignKey(Publication,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
