from rest_framework import serializers
from rest_framework.reverse import reverse
from catalogue.models import Artist, Show


class ArtistSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['id', 'firstname', 'lastname', 'links']

    def get_links(self, obj):
        request = self.context.get('request')
        return {
            'self': reverse('artist-detail', kwargs={'pk': obj.id}, request=request),
            'all_artists': reverse('artist-list', request=request),
        }


class ShowSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ['id', 'title', 'slug', 'duration', 'created_in', 'bookable', 'links']

    def get_links(self, obj):
        request = self.context.get('request')
        return {
            'self': reverse('show-detail', kwargs={'pk': obj.id}, request=request),
            'all_shows': reverse('show-list', request=request),
        }