from django import forms

class CityForm(forms.Form):
    city = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите название города...',
            'id': 'city-input',
            'class': 'search-box',
        })
    )