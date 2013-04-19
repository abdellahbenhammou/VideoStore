from django.contrib.localflavor.at.at_states import STATE_CHOICES

__author__ = 'abdellah'
from django import forms

class UploadForm(forms.Form):
    file = forms.FileField(required=True)
    name = forms.CharField(required=True)
    cat = forms.ChoiceField(choices=(('Action','Action'), ('Drama','Drama'), ('Comedy','Comedy'), ('Documentary','Documentary')), required=True)
    rating = forms.ChoiceField(choices=(('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')), required=True)
    rem = forms.CharField(required=True)



