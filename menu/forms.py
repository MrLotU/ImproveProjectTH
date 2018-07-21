from django import forms
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):
    """Form for creating/updating Menus"""
    class Meta:
        model = Menu
        fields = ('season', 'items', 'expiration_date')

    def clean(self):
        """Clean the form and check the provided date"""
        super().clean()
        expiration_date = self.cleaned_data.get('expiration_date')
        try:
            datetime.strptime(expiration_date.__str__(), '%Y-%m-%d')
        except:
            raise forms.ValidationError('Please provide a valid date in the format YYYY-MM-DD')