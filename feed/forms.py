from django import forms
from projects.models import Category, Goal, Collaborator
from account.models import Country

class PostForm(forms.Form):
    title = forms.CharField(required=False)
    text = forms.CharField()
    pfile = forms.FileField(required=False)
    goal_accomplished = forms.ModelChoiceField(required=False, queryset=Goal.objects.none())

    def __init__(self, *args, **kwargs):
        goals = kwargs.pop('goals')
        super().__init__(*args, **kwargs)
        self.fields['goal_accomplished'].queryset = goals

class CommentForm(forms.Form):
    text = forms.CharField()


class SearchForm(forms.Form):
    query = forms.CharField(empty_value=None, required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
    looking_for = forms.ModelMultipleChoiceField(queryset=Collaborator.objects.all(), required=False)
    #should be hidden
    page_number = forms.IntegerField(required=False)



