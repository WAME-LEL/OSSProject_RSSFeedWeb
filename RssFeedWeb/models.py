from django.db import models


# Create your models here.
class subsData(models.Model):
    link = models.URLField(unique=True)
    date = models.DateTimeField(auto_now_add=True)