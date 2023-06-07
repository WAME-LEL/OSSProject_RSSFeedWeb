from django.db import models


# Create your models here.
class subsData(models.Model):
    link = models.URLField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

class scrapData(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField(unique=True)
    main_title = models.CharField(max_length=100)