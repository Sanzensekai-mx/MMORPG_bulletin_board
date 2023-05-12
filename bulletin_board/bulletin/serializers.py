from rest_framework import serializers
from .models import Post, Media, Reply


class AcceptReplyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('id', 'is_accept')


class RejectReplyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('id', 'is_rejected')