from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=30)
    username = models.CharField(max_length=30, null=True)
    phone = models.PositiveIntegerField(null=True)


class Video(models.Model):
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=30)
    rating = models.PositiveIntegerField()
    remarks = models.CharField(max_length=200, null=True)
    timeOfUpload = models.DateField()
    path = models.CharField(max_length=200)

class Sessions(models.Model):
    session_id = models.CharField(max_length=10)



