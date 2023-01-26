from django.db import models
from django.utils import timezone

class FundamentalAnalysis(models.Model):
    name = models.CharField(max_length=30)
    industry = models.CharField(max_length=30)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
