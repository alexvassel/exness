from django import forms

from tom.settings import STATE_TAXES

RELEVANCE_CHOICES = (
    ((state, state) for state in STATE_TAXES)
)


class TomForm(forms.Form):
    price = forms.FloatField(label='Price per one good', min_value=0.1,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    number = forms.IntegerField(label='Number of goods', min_value=1,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.ChoiceField(label='State', choices=RELEVANCE_CHOICES,
                              widget=forms.Select(attrs={'class': 'form-control'}))
