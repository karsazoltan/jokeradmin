from django.db import models


# Create your models here.
class NodeStat(models.Model):
    date = models.DateTimeField()
    node_name = models.CharField(max_length=50)
    cpu = models.FloatField()
    mem = models.FloatField()
