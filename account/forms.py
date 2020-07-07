from django import forms
from account.models import Country, User
from account.validators import validate_username, validate_email_extension
from django.core.validators import validate_email

class EntrepreneurSignup(forms.Form): 
    invite_code = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField(max_length = 30, validators=[validate_username])
    bio = forms.CharField()
    email = forms.CharField(validators=[validate_email, validate_email_extension])
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    country = forms.ModelChoiceField(queryset = Country.objects.all())
    street_address = forms.CharField()
    city = forms.CharField()
    postcode = forms.CharField(max_length = 10)
    phone_number = forms.CharField(max_length = 15)
    profile_picture = forms.ImageField()
    #identification = forms.ImageField()

    def clean(self):
        cleaned_data = super(EntrepreneurSignup, self).clean()
        if 'password' in cleaned_data and 'confirm_password' in cleaned_data and cleaned_data['password'] != cleaned_data['confirm_password']:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

class ContributorSignup(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField(max_length = 30, validators=[validate_username])
    bio = forms.CharField(required=False)
    country = forms.ModelChoiceField(queryset = Country.objects.all())
    email = forms.CharField(validators=[validate_email, validate_email_extension])
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    profile_picture = forms.ImageField(required=False)
    def clean(self):
        cleaned_data = super(ContributorSignup, self).clean()
        if 'password' in cleaned_data and 'confirm_password' in cleaned_data and cleaned_data['password'] != cleaned_data['confirm_password']:
            self.add_error('confirm_password', 'Passwords do not match')
        return cleaned_data

class SignInForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length =32)

class BioUpdateForm(forms.Form):
    text = forms.CharField()

######## django contrib-auth has views for this
#
#class PasswordChangeForm(forms.Form):
#    old_password = forms.CharField()
#    new_password = forms.CharField()
#    confirm_password = forms.CharField()
#
#    def clean(self):
#        cleaned_data = super(ContributorSignup, self).clean()
#        if 'new_password' in cleaned_data and 'confirm_password' in cleaned_data and cleaned_data['new_password'] != cleaned_data['confirm_password']:
#            self.add_error('confirm_password', 'Passwords do not match')
#        return cleaned_data
#
#########






    

