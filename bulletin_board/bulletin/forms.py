from django import forms
from django.core.validators import FileExtensionValidator

from django.forms.models import inlineformset_factory, BaseInlineFormSet

from .models import Post, Media


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


# MediaFormset = inlineformset_factory(Post, Media, extra=1)


# class MediaForm(forms.ModelForm):
#     class Meta:
#         model = Media
#         fields = ['upload_file', ]

class MediaForm(forms.Form):
    upload_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'mp4'])]
    )