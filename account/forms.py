from django import forms
from models import Country

class EntrepeneurSignup(forms.Form): 
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField(max_length = 30, validators=[validate_username])
    e-mail = form.CharField(validators=[validate_email])
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    country = forms.ChoiceField(choices = Country.objects.all())
    street_address = forms.CharField()
    city = forms.CharField()
    postcode = forms.CharField(max_length = 10)
    phone_number = forms.CharField(max_length = 15)
    identification = forms.ImageField()

    def clean(self):
        cleaned_data = super(EntrepeneurSignup, self).clean()
        if 'password' in cleaned_data and 'confirm_password' in cleaned_data and cleaned_data['password'] != cleaned_data['confirm_password']:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

class ContributorSignup(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField(max_length = 30, validators=[validate_username])
    country = forms.ChoiceField(choices = Country.objects.all())
    e-mail = form.CharField(validators=[validate_email, validate_email_extension])
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(ContributorSignup, self).clean()
        if 'password' in cleaned_data and 'confirm_password' in cleaned_data and cleaned_data['password'] != cleaned_data['confirm_password']:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

class SignInForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length =32)

def validate_email_extension (value):
    valid = (value.endswith('.com') or value.endswith('.ca') or value.endswith('.net') or value.endswith('.org') or value.endswith('.edu'))
    if not valid:
        raise ValidationError ('Invalid E-mail format', code='invalid_email')
    email = User.objects.filter(email=value)
    if email is not None:
        raise ValidationError('Email is taken', code='email_taken')

def validate_username (value):
    user = User.objects.filter(username=value)
    if user is not None:
        raise ValidationError('Username is taken', code='username_taken')

#def validate_password (value):
#password requirements



    

