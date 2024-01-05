from django import forms
from django.utils.safestring import mark_safe
from . import views

class searchURL(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YouTube, TikTok, Facebook, Instagram, X (Twitter) video URL', 'class': 'form-control'}))
