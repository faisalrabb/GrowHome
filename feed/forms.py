from django import forms
from projects.models import Category

class PostForm(forms.Form, activity.Activity):
    title = forms.CharField(required=False)
    text = forms.CharField()
    pfile = forms.FileField(upload_to='gallery', required=False, empty_value=None)
    goal_accomplished = forms.ChoiceField(required=False, empty_value=None)

    def __init__(self, *args, **kwargs):
        goals = kwargs.pop('goals')
        super().__init__(*args, **kwargs)
        self.fields['goal_accomplished'].choices = goals



class SearchForm(forms.Form):
    term = forms.CharField(empty_value='')
    country = forms.ChoiceField(choices=Country.objects.all(), required=False, empty_value=None)