# projects/forms.py

from django import forms
from .models import Group, UserGroupSelection

class UserGroupSelectionForm(forms.ModelForm):
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = UserGroupSelection
        fields = ['group']
