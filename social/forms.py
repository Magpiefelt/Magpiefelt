from django import forms
from .models import Newsletter

class NewsletterForm(forms.ModelForm):
    """Form for newsletter signup"""
    class Meta:
        model = Newsletter
        fields = ['email', 'first_name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'px-4 py-2 w-full rounded-l focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Your email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'px-4 py-2 w-full rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-2',
                'placeholder': 'Your name (optional)'
            })
        }
