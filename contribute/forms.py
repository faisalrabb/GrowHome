from django import forms

class PledgeForm(forms.Form):
    amount = forms.IntegerField()

    