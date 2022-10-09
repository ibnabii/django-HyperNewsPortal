from django.db import models

class News(models.Model):
    description = models.TextField(null=True, blank=True)


