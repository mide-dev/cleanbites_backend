from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import PlaceDetail, PlaceReview, UserFavorite, User

# create user serializer
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['id', 'password', 'email', 'first_name', 'last_name']

# user serializer
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'password', 'email', 'first_name', 'last_name']

# add custom field to access token payload
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # custom fields
        token["firstname"] = user.first_name
        token["lastname"] = user.last_name
        token["email"] = user.email

        return token

# places serializer
class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceDetail
        fields = (
            'id',
            'business_name',
            'hygiene_score',
            'google_review_score',
            'google_review_count',
            'google_place_id',
            'street',
            'city',
            'post_code',
        )

# place detail serializer
class PlaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceDetail
        fields = ('__all__')

# place review serializer
class PlaceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceReview
        fields = ('__all__')

# user favorite serializer
class UserFavoriteSerializer(serializers.ModelSerializer):
    place = PlacesSerializer()

    class Meta:
        model = UserFavorite
        fields = ['place']