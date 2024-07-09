from django import forms
from .models import Asset, AssetImage

class AssetCreateForm(forms.ModelForm):
    images = forms.ImageField(required=True, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control m-3', 'accept': 'image/*'}), label='Upload Image')

    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'status', 'images']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control m-3', 'placeholder': 'Enter asset name', 'required': True, 'autofocus': True, 'autocomplete': 'on'}),
            'asset_type': forms.Select(attrs={'class': 'form-control m-3'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input m-3'}),
        }


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control m-3', 'placeholder': 'Enter asset name', 'required': True, 'autofocus': True, 'autocomplete': 'on'}),
            'asset_type': forms.Select(attrs={'class': 'form-control m-3'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input m-3'}),
        }


class AssetImageForm(forms.ModelForm):
    class Meta:
        model = AssetImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control m-3', 'accept': 'image/*', 'required':True})
        }
        labels = {
            'image': 'Upload More Images'
        }

