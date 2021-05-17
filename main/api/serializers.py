from django.conf import settings
from rest_framework import serializers

from django.contrib.auth.models import User
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from accounts.models import Profile
from taggit.models import Tag
from ..models import Color, Image, UsersActions


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
        fields = ('id', 'username', 'first_name', 'last_name', 'profile',)


class UsersActionsSerializer(serializers.ModelSerializer):
    image = serializers.ReadOnlyField(source='image.id')
    user = UserSerializer(read_only=True)

    class Meta:
        model = UsersActions
        fields = ('image', 'user', 'downloaded', 'vote')


class ImagesSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(read_only=True, many=True)
    tags = TagListSerializerField(read_only=True)
    author = UserSerializer(read_only=True)
    usersactions_set = UsersActionsSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = (
            'id', 'image', 'preview_image', 'image_hash', 'colors', 'title', 'tags', 'slug',
            'rating', 'width', 'height', 'ratio', 'downloads', 'size', 'extension', 'author',
            'moderator', 'usersactions_set', 'status', 'created_at', 'updated_at',
        )


class EditTagsSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Image
        fields = ('tags',)

    def validate(self, data):
        if len(data['tags']) < settings.IMAGE_MINIMUM_TAGS:
            raise serializers.ValidationError({"tags": 'There must be at least %d tags' % settings.IMAGE_MINIMUM_TAGS})
        return data


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
