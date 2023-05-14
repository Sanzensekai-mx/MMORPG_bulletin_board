from django import forms
from django.core.validators import FileExtensionValidator

from django.forms.models import inlineformset_factory, BaseInlineFormSet

from .models import Post, Media, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'wrap': 'hard', 'cols': '60'})
        }


# MediaFormset = inlineformset_factory(Post, Media, extra=1)


# class MediaForm(forms.ModelForm):
#     class Meta:
#         model = Media
#         fields = ['upload_file', ]

class MediaForm(forms.Form):
    upload_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'mp4'])],
        required=False
    )


class ReplyTextArea(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text', ]


class SendNewsMails(forms.Form):
    subject = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
