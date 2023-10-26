from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import PlaceDetail
from .fetch_external_api.place_photo import get_place_photos_reference


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['id', 'username', 'password', 'email', 'first_name', 'last_name']


class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceDetail
        fields = (
            'business_name',
            'hygiene_score',
            'google_review_score',
            'google_review_count',
            'google_place_id',
            'street',
            'city',
            'post_code',
        )


class PlaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceDetail
        fields = (
            'business_name',
            'hygiene_score',
            'google_review_score',
            'google_review_count',
            'google_place_id',
            'street',
            'city',
            'post_code',
            'latitude',
            'longitude',
        )
