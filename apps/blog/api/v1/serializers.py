from rest_framework import serializers
from apps.blog.models import BlobCategory, Content


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlobCategory
        fields = ('id', 'title')


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('id', 'title', 'category', 'description')
