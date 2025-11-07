"""
Forms for farm and field management.
"""
from django import forms
from .models import Farm, Field


class FarmForm(forms.ModelForm):
    """Form for creating and editing farms."""
    
    class Meta:
        model = Farm
        fields = ('name', 'latitude', 'longitude', 'area', 'soil_type')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Farm name'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Latitude',
                'step': 'any'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Longitude',
                'step': 'any'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Area in hectares',
                'step': '0.01',
                'min': '0.01'
            }),
            'soil_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['soil_type'].required = False


class FieldForm(forms.ModelForm):
    """Form for creating and editing fields."""
    
    class Meta:
        model = Field
        fields = ('farm', 'name', 'latitude', 'longitude', 'area')
        widgets = {
            'farm': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Field name'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Latitude (optional)',
                'step': 'any'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Longitude (optional)',
                'step': 'any'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Area in hectares',
                'step': '0.01',
                'min': '0.01'
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filter farms to only show user's farms
            self.fields['farm'].queryset = Farm.objects.filter(user=user)
            # Make farm required if creating new field
            if not self.instance.pk:
                self.fields['farm'].required = True

