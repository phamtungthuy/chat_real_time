from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)