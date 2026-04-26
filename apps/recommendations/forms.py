"""
Forms for crop recommendations.
"""
from django import forms
from apps.farms.models import Field, Farm


class RecommendationRequestForm(forms.Form):
    """Form for requesting crop recommendations from existing fields."""
    
    farm = forms.ModelChoiceField(
        queryset=Farm.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
        }),
        help_text="Select a farm to get crop recommendations"
    )
    
    include_weather = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        help_text="Include current weather data in recommendations"
    )
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['farm'].queryset = Farm.objects.filter(user=user)


class MagicRecommendationForm(forms.Form):
    """Form for requesting crop recommendations via the Magic Flow (auto-create setup)."""
    
    farm_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'E.g., North Valley Farm'
        })
    )
    
    area = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Area in hectares',
            'step': '0.01'
        })
    )
    
    latitude = forms.FloatField(
        required=True,
        widget=forms.HiddenInput()
    )
    
    longitude = forms.FloatField(
        required=True,
        widget=forms.HiddenInput()
    )

