from django import forms
from projects.models import Category

class PostForm(forms.Form):
    title = forms.CharField(required=False)
    text = forms.CharField()
    pfile = forms.FileField(upload_to='gallery', required=False, empty_value=None)
    goal_accomplished = forms.ModelChoiceField(required=False, empty_value=None)

    def __init__(self, *args, **kwargs):
        goals = kwargs.pop('goals')
        super().__init__(*args, **kwargs)
        self.fields['goal_accomplished'].queryset = goals

class CommentForm(forms.Form):
    text = forms.CharField()


class SearchForm(forms.Form):
    query = forms.CharField(empty_value=None, required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, empty_value=None)
    looking_for = forms.ModelMultipleChoiceField(queryset=Collaborator.objects.all(), required=False, empty_value=None)
    #should be hidden
    page_number = forms.IntegerField(default=0, required=False)



