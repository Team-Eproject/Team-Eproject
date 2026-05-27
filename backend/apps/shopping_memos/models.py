from django.db import models

class Memo(models.Model):
    title = models.CharField(max_length=255, blank=True)

    content = models.TextField(blank=True)