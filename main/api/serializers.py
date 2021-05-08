from rest_framework import serializers

from django.contrib.auth.models import User
from taggit_serializer.serializers import TagListSerializerField
from accounts.models import Profile
from ..models import Color, Image, ImageFollowers


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('hex',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('photo',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'profile',)


class ImageFollowersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ImageFollowers
        fields = ('user', 'downloaded', 'vote',)


class ImagesSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(read_only=True, many=True)
    tags = TagListSerializerField(read_only=True)
    followers = ImageFollowersSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Image
        fields = (
            'id', 'image', 'preview_image', 'image_hash', 'colors', 'tags', 'slug', 'rating', 'width', 'height', 'ratio',
            'downloads', 'size', 'extension', 'author', 'moderator', 'followers', 'status', 'created_at', 'updated_at',
        )