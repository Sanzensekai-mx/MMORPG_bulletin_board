from django import forms
from .models import Post, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Изображение",
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

    class Meta:
        model = Image
        fields = ['upload_image',]