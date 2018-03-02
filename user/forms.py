from django import forms
from django.core.exceptions import ValidationError


class UserInfoForm(forms.Form):
    email = forms.EmailField(label='邮箱', required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '用于找回密码'}))
    nickname = forms.CharField(max_length=60, label='昵称', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '叫你什么好呢？'}))
    icon = forms.ImageField(label='头像', required=False,
                            widget=forms.FileInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(label='生日', required=False,
                               widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control',
                                                             'min': '1911-01-01'}))
    sex = forms.ChoiceField(label='性别', choices=((0, '保密'), (1, '男'), (2, '女')),
                            widget=forms.Select(attrs={'class': 'form-control'}))
    signature = forms.CharField(max_length=120, label='简介', required=False,
                                widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '随便写点什么呗'}))


class RegisterForm(forms.Form):

    username = forms.CharField(max_length=60, label='账号',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '登录后可再设昵称'}))

    password1 = forms.CharField(max_length=60, label='密码',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': '密码不少于六位'}))

    password2 = forms.CharField(max_length=60, label='确认',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': '请再次确认密码'}))

    def is_valid(self):
        res = super().is_valid()
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise ValidationError('前后密码不一致')
        return res