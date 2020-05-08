from django import forms
from models import Country

class EntrepeneurSignup(forms.Form): 
    first_name = forms.CharField(max_length='20')
    last_name = forms.CharField(max_length='25')
    username = forms.CharField(max_length = '30', validators=[validate_username])
    e-mail = form.TextField(validators=[validate_email])
    password = forms.CharField(max_length='32', widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length='32', widget=forms.PasswordInput)
    country = forms.ChoiceField(choices = Country.objects.all())
    street_address = forms.TextField()
    city = forms.TextField()
    postcode = forms.CharField(max_length = '10')
    phone_number = forms.CharField(max_length = '15')
    identification = forms.ImageField()

    def clean(self):
        cleaned_data = super(EntrepeneurSignup, self).clean()
        if 'password' in cleaned_data and 'confirm_password' in cleaned_data and cleaned_data['password'] != cleaned_data['confirm_password']:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

class ContributorSignup(forms.Form):
    first_name = forms.CharField(max_length='20')
    last_name = forms.CharField(max_length='25')
    username = forms.CharField(max_length = '30', validators=[validate_username])
    country = forms.ChoiceField(choices = Country.objects.all())
    e-mail = form.TextField(validators=[validate_email])
    password = forms.CharField(max_length='32', widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length='32', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(ContributorSignup, self).clean()
        if 'password' in cleaned_data and 'confirm_password' in cleaned_data and cleaned_data['password'] != cleaned_data['confirm_password']:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

class SignInForm(forms.Form):
    username = forms.CharField(max_length='30')
    password = forms.CharField(max_length ='32')

def validate_email (value):
    valid = (value.endswith('.com') or value.endswith('.ca') or value.endswith('.net'))
    if not valid:
        raise ValidationError ('Invalid E-mail format', code='invalidEmail')
    email = User.objects.filter(email=value)
    if email is not None:
        raise ValidationError('Email not available', code='invalidEmail')

def validate_username (value):
    user = User.objects.filter(username=user)
    if user is not None:
        raise ValidationError('Username is taken', code='invalidUsername')
    



    

