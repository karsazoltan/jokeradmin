from django.db import models


# Create your models here.
class Notice(models.Model):
    subject = models.CharField(max_length=50)
    body = models.TextField(max_length=800)
    date = models.DateTimeField()
    editor = models.ForeignKey()