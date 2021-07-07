from django.db import models
from django.contrib.auth.models import User
class Github(models.Model):
    githubuser = models.CharField(max_length=1000)
    imagelink = models.CharField(max_length=10000)
    username = models.CharField(max_length=1000)


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=200)
    verify=models.BooleanField(default=False)
    

class Quaries(models.Model):
    email=models.EmailField()
    msg=models.TextField()  