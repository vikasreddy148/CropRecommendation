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
    """Form for requesting crop recommendations via the Magic Flow (manual data entry)."""
    
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
        initial=1.0,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Area in hectares',
            'step': '0.01'
        })
    )
    
    # Soil Properties
    nitrogen = forms.FloatField(
        required=True,
        label="Nitrogen (N)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ratio of Nitrogen content in soil',
            'step': '1'
        })
    )
    
    phosphorus = forms.FloatField(
        required=True,
        label="Phosphorus (P)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ratio of Phosphorous content in soil',
            'step': '1'
        })
    )
    
    potassium = forms.FloatField(
        required=True,
        label="Potassium (K)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ratio of Potassium content in soil',
            'step': '1'
        })
    )
    
    ph = forms.FloatField(
        required=True,
        label="pH Level",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'pH value of the soil (0-14)',
            'step': '0.1',
            'min': '0',
            'max': '14'
        })
    )
    
    # Weather Properties
    temperature = forms.FloatField(
        required=True,
        label="Temperature (°C)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Temperature in degree Celsius',
            'step': '0.1'
        })
    )
    
    humidity = forms.FloatField(
        required=True,
        label="Humidity (%)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Relative humidity in %',
            'step': '0.1',
            'min': '0',
            'max': '100'
        })
    )
    
    rainfall = forms.FloatField(
        required=True,
        label="Rainfall (mm)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rainfall in mm',
            'step': '0.1'
        })
    )


