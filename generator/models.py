from __future__ import unicode_literals

from django.db import models

# Create your models here.

class traffic(models.Model):
   id_empresa = models.PositiveIntegerField(default=1)
   empresa = models.CharField(max_length=200, blank=True)
   cliente_id = models.PositiveIntegerField(default=1)
   ip_visited = models.CharField(max_length=200,  blank=True)
   download = models.FloatField()
   time = models.DateTimeField()
