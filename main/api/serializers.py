from rest_framework import serializers

from main.models import Image


class ImageSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'image', 'tag', 'url')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = {"id": instance.author.id, "username": instance.author.username}
        return representation
