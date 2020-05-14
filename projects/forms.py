from django import forms
from projects.models import Category
from account.models import Country


class ProjectForm(forms.Form):
    country = forms.ChoiceField(choices = Country.objects.all())
    city = forms.CharField()
    name = forms.CharField()
    problem = forms.CharField()
    solution = forms.CharField()
    category = forms.ChoiceField(choices=Category.objects.all())
    info = forms.CharField()
    funding_goal = forms.IntegerField()
    goal_1 = forms.CharField()
    goal_2 = forms.CharField()
    goal_3 = forms.CharField()
    info = forms.CharField()
    video = forms.FileField(validators=[validate_file])
    photo = forms.ImageField(validators=[validate_image])
    intro_video = forms.FileField(validators=[validate_file])
    photo = forms.ImageField(validators=[validate_image])

class FundingRoundForm(forms.Form):
    funding_goal = forms.IntegerField(max_value=20000)
    goal_1 = forms.CharField()
    goal_2 = forms.CharField()
    goal_3 = forms.CharField()
    info = forms.CharField()
    video = forms.FileField(validators=[validate_file])
    #photo = forms.ImageField(validators=[validate_image])
    note = forms.CharField(blank=True)
    
class ProjectUpdateForm(forms.Form):
    name = forms.CharField()
    problem = forms.CharField()
    solution = forms.CharField()
    city = forms.CharField()
    video = forms.FileField(required=False)


def validate_file (value): 
    if value is None:
        raise ValidationError('This field is required', code='empty_video')
    else if not value.endswith('.mp4'):
        raise ValidationError('Invalid file format: videos must be mp4 format!')
    

def validate_image (value):
    if value is None:
        raise ValidationError('This field is required', code='empty_image')
    else if not value.endswith('.jpeg') or value.endswith('.jpg') or value.endswith('.png')
        raise ValidationError('Only accepted image formats are: jpg, jpeg, png')

