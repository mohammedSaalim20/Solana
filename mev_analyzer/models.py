from django.db import models


class MEVTransaction(models.Model):
    tx_hash = models.CharField(max_length=100, unique=True)
    wallet = models.CharField(max_length=100)
    path = models.TextField()
    platforms = models.TextField()
    profit = models.FloatField()
    is_mev = models.BooleanField()
    pattern = models.TextField()
    timestamp = models.DateTimeField()
