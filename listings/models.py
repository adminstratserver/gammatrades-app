from django.db import models
from django.utils import timezone
from members.models import Member
from .choices import document_choices


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100, default=None)
    contributor = models.ForeignKey(Member, null=True, blank=True, on_delete=models.CASCADE)
    list_date = models.DateTimeField(default=timezone.now, blank=False)
    is_published = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=document_choices, default="proposal")
    document_file = models.FileField(upload_to='listings/documents/%Y/%m/%d/')
    cover_file = models.ImageField(upload_to='listings/covers/%Y/%m/%d/', default="listings/default/preview1.png")
    image1_file = models.ImageField(upload_to='listings/previews/%Y/%m/%d/', default="listings/default/preview1.png")
    image2_file = models.ImageField(upload_to='listings/previews/%Y/%m/%d/', default="listings/default/preview1.png")
    image3_file = models.ImageField(upload_to='listings/previews/%Y/%m/%d/', default="listings/default/preview1.png")

    def __str__(self):
      return self.title

    def delete(self, *args, **kwargs):
      self.document_file.delete()
      self.cover_file.delete()
      self.image1_file.delete()
      self.image2_file.delete()
      self.image3_file.delete()
      super().delete(*args, **kwargs)