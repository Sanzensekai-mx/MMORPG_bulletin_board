from rest_framework import serializers
from .models import Post, Media


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'image')


class PostSerializer(serializers.ModelSerializer):
    upload_files = ImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'category', 'upload_files')
