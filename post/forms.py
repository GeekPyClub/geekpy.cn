from django import forms
from django.core.exceptions import ValidationError




class createForm(forms.Form):

    title = forms.CharField(max_length=24, label='标题',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '二十字内概括你的内容'}))

    body = forms.CharField(max_length=6400, label='内容',
                                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '20',
                                                                  'placeholder': '六千字够您产所欲言了吧？'}))
