from django import forms
from .models import Review


class ProductReviewForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.Textarea(attrs={'class': 'form-control', 'cols': 30, "rows": 15})
    
    class Meta:
        model = Review
        fields = ['name', 'content']