from django import forms

from .models import Site


class SiteForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Site
        fields = ['name', 'description', 'url', 'github']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'input m-2',
                    'placeholder': 'Project Name',
                    'required': 'required'
                }),
            'description': forms.Textarea(attrs={'class': 'textarea m-2', 'placeholder': 'Project Description'}),
            'url': forms.URLInput(attrs={'class': 'input m-2', 'placeholder': 'Project URL'}),
            'github': forms.URLInput(attrs={'class': 'input m-2', 'placeholder': 'Github URL'}),
        }
