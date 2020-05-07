from django import forms
from models import Country

class EntrepeneurSignup(forms.Form): 
    first_name = forms.CharField(max_length='20')
    last_name = form.CharField(max_length='25')
    username = forms.CharField(max_length = '30')
    e-mail = form.TextField()
    password = models.CharField(max_length='32', widget=forms.PasswordInput)
    confirm_password = models.CharField(max_length='32', widget=forms.PasswordInput)
    country = forms.ChoiceField(choices = Country.objects.all())
    street_address = models.TextField()
    city = models.TextField()
    postcode = models.CharField(max_length = 10)
    phone_number = models.CharField(max_length = 12)
    identification = models.ImageField()


    

