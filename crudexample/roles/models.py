from django.db import models

class Roles(models.Model):
    id = models.AutoField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
