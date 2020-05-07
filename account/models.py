from django.db import models
from django.contrib.auth import user
from projects.models import Project

# Create your models here.

class Entrepeneur(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #project = models.OneToOneField(Project, on_delete=models.CASCADE) - deleted, connect through other side (one to one from project to entrepeneur instance)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    address = models.TextField()
    identification = models.OneToOneField(Identification, on_delete=models.SET_NULL)


class Identification(models.Model):
    file = models.ImageField(upload_to'id')


class Contributor(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    following = models.ManyToManyField(Entrepeneur, related_name='following')

class Country(models.Model):
    name = models.CharField(max_length = 15)


