from django import forms
from projects.models import Category, Collaborator
from account.models import Country
from projects.validators import validate_image, validate_file


class ProjectForm(forms.Form):
    city = forms.CharField()
    name = forms.CharField(max_length=80)
    problem = forms.CharField()
    solution = forms.CharField()
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label= "Please choose a category")
    info = forms.CharField()
    video = forms.FileField(validators=[validate_file])
    photo = forms.ImageField(validators=[validate_image])
    looking_for = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Collaborator.objects.all())

class FundingRoundForm(forms.Form):
    funding_goal = forms.IntegerField(max_value=10000)
    goal_1 = forms.CharField()
    goal_2 = forms.CharField()
    goal_3 = forms.CharField()
    info = forms.CharField()
    video = forms.FileField(validators=[validate_file], required=False)
    note = forms.CharField(required=False)

class FundingRoundUpdateForm(forms.Form):
    funding_goal = forms.IntegerField(max_value=20000)
    info = forms.CharField()
    video = forms.FileField(validators=[validate_file])
    note = forms.CharField(required=False)

class AddGoalForm(forms.Form):
    text = forms.CharField()

