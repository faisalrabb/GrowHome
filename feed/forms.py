from django import forms
from projects.models import Category

class PostForm(forms.Form, activity.Activity):
    title = forms.CharField(blank=True,null=True)
    text = forms.CharField()
    pfile = forms.FileField(upload_to='gallery', null=True, blank=True, empty_value=None)
    goal_accomplished = forms.ChoiceField(choices=[1,2,3], blank=True, null=True, empty_value=None)

class PostUpdateForm(forms.Form):
    title = forms.CharField(blank=True,null=True)
    text = forms.CharField()
    pfile = forms.FileField(upload_to='gallery', null=True, blank=True, empty_value=None)
    goal_accomplished = forms.ChoiceField(choices=[1,2,3], blank=True, null=True, empty_value=None)