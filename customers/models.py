from django.db import models
from members.models import Member

class Customer(models.Model):
	salesrep = models.ForeignKey(Member, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, null=True)
	country = models.CharField(max_length=50, null=True)
	agent = models.CharField(max_length=100, default="NIL")
	profile_pic = models.ImageField(default="photos/pic1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

	def delete(self, *args, **kwargs):
		self.profile_pic.delete()
		super().delete(*args, **kwargs)


