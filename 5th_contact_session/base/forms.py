from django import forms

from .models import Media


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'description', 'file', 'media_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*,audio/*',
            }),
            'media_type': forms.Select(attrs={'class': 'form-select'}),
        }
