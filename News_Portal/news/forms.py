from django import forms
from django.contrib.auth.models import User

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categories',
            'title',
            'content',
        ]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
