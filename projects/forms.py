from django import forms
from projects.models import Category
from account.models import Country


class ProjectForm(forms.Form):
    city = forms.CharField()
    name = forms.CharField(max_length=80)
    problem = forms.CharField()
    solution = forms.CharField()
    category = forms.ChoiceField(choices=Category.objects.all(), required=False, empty_value=None)
    info = forms.CharField()
    video = forms.FileField(validators=[validate_file])
    photo = forms.ImageField(validators=[validate_image])
    looking_for = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=Collaborator.objects.all())

class FundingRoundForm(forms.Form):
    funding_goal = forms.IntegerField(max_value=10000)
    goal_1 = forms.CharField()
    goal_2 = forms.CharField()
    goal_3 = forms.CharField()
    info = forms.CharField()
    video = forms.FileField(validators=[validate_file], required=False, empty_value=None)
    note = forms.CharField(required=False, empty_value=None)

class FundingRoundUpdateForm(forms.Form):
    funding_goal = forms.IntegerField(max_value=20000)
    info = forms.CharField()
    video = forms.FileField(validators=[validate_file])
    note = forms.CharField(blank=True)

class AddGoalForm(forms.Form):
    text = forms.CharField()

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

