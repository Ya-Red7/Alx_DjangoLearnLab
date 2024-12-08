from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post, Tag
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Separate tags with commas.")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Add tags separated by commas',
            }),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        tags = self.cleaned_data['tags'].split(',')
        if commit:
            instance.save()
            instance.tags.set(Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags)
        return instance