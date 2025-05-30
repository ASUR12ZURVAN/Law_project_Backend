from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    email_id = models.CharField(max_length = 500,unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name

