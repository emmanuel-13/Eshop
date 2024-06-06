from django import forms

from .models import *


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "cols": 10, "rows": 2}))
    class Meta:
        model = Comment
        exclude = ['user', 'blog', 'new']
        fields = ("comment",)