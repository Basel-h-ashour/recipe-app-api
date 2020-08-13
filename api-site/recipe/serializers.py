from rest_framework import serializers

from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """serializes json data into tag objects and vice-versa"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
