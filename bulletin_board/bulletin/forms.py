from django import forms
from .models import Post, Media


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


class ImageForm(forms.ModelForm):
    image = forms.FileField(
        label="Изображение",
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

    class Meta:
        model = Media
        fields = ['upload_file',]