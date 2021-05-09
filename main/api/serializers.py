from rest_framework import serializers

from django.contrib.auth.models import User
from taggit_serializer.serializers import TagListSerializerField
from accounts.models import Profile
from ..models import Color, Image, ImageUserActions


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


class ImagesSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(read_only=True, many=True)
    tags = TagListSerializerField(read_only=True)
    image_user_actions = serializers.ReadOnlyField(source='image_user_actions_set')
    author = UserSerializer(read_only=True)

    class Meta:
        model = Image
        fields = (
            'id', 'image', 'preview_image', 'image_hash', 'colors', 'title', 'tags', 'slug',
            'rating', 'width', 'height', 'ratio', 'downloads', 'size', 'extension', 'author',
            'moderator', 'image_user_actions', 'status', 'created_at', 'updated_at',
        )


class ImageUserActionsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    image = serializers.ReadOnlyField(source='image.id')

    class Meta:
        model = ImageUserActions
        fields = ('user', 'image', 'downloaded', 'vote')
