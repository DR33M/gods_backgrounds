from rest_framework import serializers

from django.contrib.auth.models import User
from taggit_serializer.serializers import TagListSerializerField
from accounts.models import Profile
from ..models import Color, Image, UserImage


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
        fields = ('first_name', 'last_name', 'profile',)


class ImagesSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(read_only=True, many=True)
    tags = TagListSerializerField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Image
        fields = (
            'image', 'preview_image', 'image_hash', 'colors', 'tags', 'slug', 'rating', 'width', 'height', 'ratio',
            'downloads', 'author', 'moderator', 'status', 'created_at', 'updated_at',
        )


class UserImageSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(read_only=True, many=True)
    tags = TagListSerializerField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = UserImage
        fields = ('user', 'image', 'downloaded', 'vote', 'download',)
