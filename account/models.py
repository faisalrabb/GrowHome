from django.db import models
from django.contrib.auth import user


# Create your models here.

class Entrepeneur(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    about = models.TextField(null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length =15)
    #identification = models.OneToOneField(Identification, on_delete=models.SET_NULL)

    def __str__(self):
        return user.username


# --> uncomment this model if implementing ID check
#class Identification(models.Model):
#    file = models.ImageField(upload_to='id')


class Contributor(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    profile_picture = models.ImageField(upload_to='/photos')
    #following = models.ManyToManyField(Entrepeneur, related_name='following', null=True, blank=True)

    def __str__(self):
        return user.username

class Key(models.Model):
    key = models.CharField(max_length=10)
    used = models.BooleanField(default=False)

class Country(models.Model):
    name = models.CharField(max_length = 15)#, null=True)
    def __str__(self):
        return self.name


